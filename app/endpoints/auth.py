from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt_auth import create_access_token
from app.auth.password_utils import verify_password
from app.schemas.auth import Token
from app.models.user import User as UserModel

router = APIRouter()

# Duración del token de acceso (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un token JWT usando nombre de usuario y contraseña.
    """
    # Buscar el usuario en la base de datos
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está deshabilitado
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario deshabilitado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear los datos del token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint de ejemplo para crear un usuario (solo para pruebas)
@router.post("/create_user")
async def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear un nuevo usuario. 
    En una aplicación real, esto probablemente debería tener más validación y seguridad.
    """
    from app.auth.password_utils import get_password_hash
    
    # Verificar si el usuario ya existe
    existing_user = db.query(UserModel).filter(
        (UserModel.username == username) | (UserModel.email == email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario o correo electrónico ya existe"
        )
    
    # Crear el nuevo usuario con la contraseña hasheada
    hashed_password = get_password_hash(password)
    db_user = UserModel(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Usuario creado exitosamente", "username": db_user.username}