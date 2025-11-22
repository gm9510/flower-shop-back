import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

# Configuración desde variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Esto no se usará con RSA
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Variables globales para almacenar el par de claves
_PRIVATE_KEY = None
_PUBLIC_KEY = None

def generate_rsa_keys():
    """Generar par de claves RSA para firmado y verificación de JWT."""
    global _PRIVATE_KEY, _PUBLIC_KEY
    
    if _PRIVATE_KEY is None or _PUBLIC_KEY is None:
        # Generar una nueva clave privada
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Obtener la clave pública correspondiente
        public_key = private_key.public_key()
        
        # Almacenar las claves
        _PRIVATE_KEY = private_key
        _PUBLIC_KEY = public_key
        
    return _PRIVATE_KEY, _PUBLIC_KEY

def get_jwk():
    """Generar y devolver un JWK (JSON Web Key) del par de claves RSA."""
    private_key, public_key = generate_rsa_keys()
    
    # Serializar la clave pública a formato PEM
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Convertir PEM a formato JWK
    # Primero, obtener los números públicos
    public_numbers = public_key.public_numbers()
    n = public_numbers.n
    e = public_numbers.e
    
    # Convertir a formato base64url
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    e_bytes = e.to_bytes((e.bit_length() + 7) // 8, 'big')
    
    n_b64 = base64.urlsafe_b64encode(n_bytes).decode('utf-8').rstrip('=')
    e_b64 = base64.urlsafe_b64encode(e_bytes).decode('utf-8').rstrip('=')
    
    # Crear el JWK
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": "flower-shop-jwk-1",  # Un identificador único para esta clave
        "n": n_b64,
        "e": e_b64
    }
    
    return jwk

def get_jwks():
    """Devolver un JWKS (JSON Web Key Set) que contiene nuestro JWK."""
    return {"keys": [get_jwk()]}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear un nuevo token de acceso con los datos proporcionados."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # Usar la clave privada para firmar el token
    encoded_jwt = jwt.encode(to_encode, generate_rsa_keys()[0], algorithm="RS256")
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """Verificar un token JWT usando nuestra clave pública."""
    try:
        # Obtener la clave pública
        _, public_key = generate_rsa_keys()
        
        # Convertir la clave pública a formato PEM para verificación
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Decodificar el token
        payload = jwt.decode(
            token, 
            pem_public_key, 
            algorithms=["RS256"],
            options={"verify_exp": True}
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

# Esquema de seguridad para FastAPI
bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict[str, Any]:
    """Dependencia de FastAPI para recuperar el usuario actual del token JWT."""
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Falta el token de autorización")

    claims = verify_token(token)
    # Devolver el diccionario de claims como el usuario
    return claims

def get_public_key_pem():
    """Obtener la clave pública en formato PEM."""
    _, public_key = generate_rsa_keys()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')