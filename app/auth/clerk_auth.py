import os
import time
import json
from typing import Dict, Any, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import httpx
from jose import jwt, JWTError
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Simple JWKS cache
_JWKS_CACHE: Dict[str, Any] = {"keys": None, "fetched_at": 0}
JWKS_TTL = int(os.getenv("CLERK_JWKS_TTL", "300"))  # seconds

bearer_scheme = HTTPBearer()


def _get_jwks_url() -> str:
    jwks = os.getenv("CLERK_JWKS_URL")
    if jwks:
        return jwks
    issuer = os.getenv("CLERK_ISSUER")
    if issuer:
        return issuer.rstrip("/") + "/.well-known/jwks.json"
    raise RuntimeError("CLERK_JWKS_URL or CLERK_ISSUER must be set in environment")


def _fetch_jwks() -> Dict[str, Any]:
    now = int(time.time())
    if _JWKS_CACHE["keys"] and (now - _JWKS_CACHE["fetched_at"] < JWKS_TTL):
        return _JWKS_CACHE["keys"]

    url = _get_jwks_url()
    try:
        resp = httpx.get(url, timeout=5.0)
        resp.raise_for_status()
        jwks = resp.json()
        _JWKS_CACHE["keys"] = jwks
        _JWKS_CACHE["fetched_at"] = now
        return jwks
    except Exception as e:
        raise RuntimeError(f"Error fetching JWKS from {url}: {e}")


def _get_signing_key(token: str) -> Dict[str, Any]:
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    if not kid:
        raise JWTError("Token header missing kid")

    jwks = _fetch_jwks()
    keys = jwks.get("keys", [])
    for key in keys:
        if key.get("kid") == kid:
            return key
    raise JWTError("Appropriate JWK not found")


def verify_token(token: str) -> Dict[str, Any]:
    """Verify Clerk JWT using JWKS. Returns the token claims on success.

    Requires CLERK_ISSUER or CLERK_JWKS_URL in environment. Optionally set CLERK_AUDIENCE.
    """
    issuer = os.getenv("CLERK_ISSUER")
    audience = os.getenv("CLERK_AUDIENCE")

    try:
        key = _get_signing_key(token)
        # Convert JWK (RSA) to a PEM public key using cryptography
        if key.get("kty") != "RSA":
            raise HTTPException(status_code=400, detail="Unsupported JWK key type")

        def _b64_to_int(b64: str) -> int:
            # base64url decode without padding
            data = b64 + "=" * ((4 - len(b64) % 4) % 4)
            raw = base64.urlsafe_b64decode(data)
            return int.from_bytes(raw, "big")

        n = _b64_to_int(key.get("n"))
        e = _b64_to_int(key.get("e"))

        public_numbers = rsa.RSAPublicNumbers(e, n)
        public_key_obj = public_numbers.public_key()
        public_key_pem = public_key_obj.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        algorithms = [key.get("alg", "RS256")]

        decode_kwargs: Dict[str, Any] = {"algorithms": algorithms}
        if audience:
            decode_kwargs["audience"] = audience
        if issuer:
            decode_kwargs["issuer"] = issuer

        claims = jwt.decode(token, public_key_pem, **decode_kwargs)
        return claims
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failure: {e}")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict[str, Any]:
    """FastAPI dependency to retrieve the current user (Clerk JWT)."""
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    claims = verify_token(token)
    # Clerk includes user id and other claims — return the claims dictionary as the user for now
    return claims
