
from datetime import datetime, timedelta
from typing import Dict
from jose import jwt
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
import random

from app.auth.service.auth_service import AuthService
from app.auth.repository.user_repository import UserRepository
from app.auth.schema.user import UserLogin, Token, User
from app.core.services.email_service import EmailService
from app.core.services.impl.email_service_impl import EmailServiceImpl
from core.exceptions import AppBaseException
from config.config import settings
from utl.security_util import SecurityUtil

# Keep in-memory for codes for now as discussed
# Structure: {email: {"code": str, "expiry": datetime}}
fake_verification_codes: Dict[str, Dict] = {}

class AuthServiceImpl(AuthService):
    def __init__(self, email_service: EmailService = None):
        self.user_repository = UserRepository()
        self.email_service = email_service or EmailServiceImpl()

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def login(self, db: AsyncSession, user_in: UserLogin) -> Token:
        # Get ORM user to check password hash
        user_orm = await self.user_repository.get_user_orm_by_email(db, user_in.email)
        
        if not user_orm:
             raise AppBaseException("Incorrect email or password", status_code=status.HTTP_400_BAD_REQUEST)
        
        if not user_orm.habilitado:
            raise AppBaseException("El usuario se encuentra inhabilitado. Por favor, contacte al administrador.", status_code=status.HTTP_403_FORBIDDEN)
        
        stored_hash = user_orm.password

        # Security check
        if not stored_hash or not SecurityUtil.verify_password(user_in.password, stored_hash):
             raise AppBaseException("Incorrect email or password", status_code=status.HTTP_400_BAD_REQUEST)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={
                "sub": user_orm.correo,
                "usuarioId": str(user_orm.usuario_id), 
                "usuario": user_orm.usuario, 
                "nombre":  f"{user_orm.primer_nombre or ''} {user_orm.segundo_nombre or ''} {user_orm.apellido_paterno or ''} {user_orm.apellido_materno or ''}".replace("  ", " ").strip(),
                "rolId": str(user_orm.rol.rol_id) if user_orm.rol else None, 
                "rolCodigo": user_orm.rol.codigo if user_orm.rol else None,
                "rol": user_orm.rol.nombre if user_orm.rol else None,
                "primerIngreso": user_orm.primer_ingreso
            }, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    async def forgot_password(self, db: AsyncSession, email: str) -> str:
        # Check if user exists in DB
        user = await self.user_repository.get_by_email(db, email)
        if not user:
            # Mask existence or throw
             raise AppBaseException("Email not registered", status_code=status.HTTP_404_NOT_FOUND)

        code = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=5)
        fake_verification_codes[email] = {"code": code, "expiry": expiry}
        
        print(f"DEBUG: Verification code for {email} is {code} (expires at {expiry} UTC)") 

        # Send email
        nombre_completo = user.full_name or "Usuario"
        email_sent = self.email_service.send_verification_code(email, code, nombre_completo)
        
        if not email_sent:
            print(f"ERROR: Failed to send verification email to {email}")

        return f"Code sent to {email}."

    async def verify_code(self, db: AsyncSession, email: str, code: str) -> bool:
        data = fake_verification_codes.get(email)
        
        if not data:
            raise AppBaseException("Invalid verification code", status_code=status.HTTP_400_BAD_REQUEST)

        stored_code = data.get("code")
        expiry = data.get("expiry")

        if stored_code != code:
            raise AppBaseException("Invalid verification code", status_code=status.HTTP_400_BAD_REQUEST)

        if datetime.utcnow() > expiry:
            del fake_verification_codes[email]
            raise AppBaseException("Verification code has expired", status_code=status.HTTP_400_BAD_REQUEST)

        return True

    async def reset_password(self, db: AsyncSession, email: str, code: str, new_password: str) -> bool:
        if not await self.verify_code(db, email, code):
             return False
        
        hashed_pwd = SecurityUtil.get_password_hash(new_password)
        success = await self.user_repository.update_password(db, email, hashed_pwd)
        
        if not success:
             raise AppBaseException("User not found", status_code=status.HTTP_404_NOT_FOUND)
             
        if email in fake_verification_codes:
            del fake_verification_codes[email]
            
        return True

    async def get_user_by_token(self, db: AsyncSession, token: str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise AppBaseException("Could not validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            raise AppBaseException("Could not validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
            
        user = await self.user_repository.get_by_email(db, email)
        if user is None:
            raise AppBaseException("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def change_password(self, db: AsyncSession, email: str, new_password: str) -> bool:
        # Check user existence
        user_orm = await self.user_repository.get_user_orm_by_email(db, email)
        if not user_orm:
             raise AppBaseException("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        hashed_pwd = SecurityUtil.get_password_hash(new_password)
        # update_password in repository already sets primer_ingreso = False
        success = await self.user_repository.update_password(db, email, hashed_pwd)
        
        if success:
            return True
        return False
