from datetime import datetime, timedelta
from typing import Optional, List, Union
from enum import Enum

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status, Request
from jose import jwt
from passlib.context import CryptContext

from certify.core.config import SECRET_KEY, JWT_ALGORITHM, DEFAULT_TOKEN_EXPIRE
from certify.constants.scope import Scope as ScopeEnum
from certify.models.token import TokenError


class CertifyAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=TokenError(
                    error_type="oauth.failed",
                    error_code=103,
                    error_description="Unable to verify OAuth. OAuth invalid or expired.",
                ),
            )

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = CertifyAuth2PasswordBearer(tokenUrl="auth")

oauth_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=TokenError(
        error_type="user.token.failed",
        error_code=102,
        error_description="OAuth token doesn't have required scope or expired.",
    ),
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain_text against hashed bcrypt hash_password
    Args:
        plain_password (str)
        hashed_password (str)
    Returns:
        bool
    """
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for given plain text password.
    Args:
        password (str)
    Returns:
        str
    """
    return PASSWORD_CONTEXT.hash(password)


def create_access_token(
    data: dict, expires_delta: Optional[Union[timedelta, None]] = None
) -> str:
    """Generate OAuth2 token with given data, and expiry
    Args:
        data (dict)
        expires_delta (Optional[Union[timedelta, None]], optional): Defaults to None.
    Returns:
        str: OAuth2 encoded token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=DEFAULT_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(
        SECRET_KEY), algorithm=JWT_ALGORITHM.value)

    return encoded_jwt

async def get_oauth_data(request: Request) -> dict:
    oauth_data = request.scope["oauth"]

    if oauth_data is None:
        raise oauth_error

    return oauth_data

def require_oauth_scopes(*scopes: List[ScopeEnum]):
    """Checks if user has required scope/permission. 
    Raises:
        oauth_error: If user doesn't have sufficient scope/perms.
    Returns:
        Depends: FastAPI dependency
    """
    scopes_req = set(map(str, scopes))

    def __check_oauth_scope(oauth_data: dict = Depends(get_oauth_data)):
        available_scopes = set(oauth_data["scopes"])

        if not scopes_req.issubset(available_scopes):
            raise oauth_error

    return Depends(__check_oauth_scope)