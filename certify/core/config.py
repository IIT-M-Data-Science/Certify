import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret, URL

from certify.constants.jwt import JWTTokenType

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config(
    "SECRET_KEY", cast=Secret, default="5df9db467ed2c905bcc1")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[]
)
LOGGING_LEVEL = (
    logging.DEBUG
    if DEBUG
    else config("LOGGING_LEVEL", cast=lambda x: getattr(logging, x), default="INFO")
)
DEFAULT_TOKEN_EXPIRE = config(
    "DEFAULT_TOKEN_EXPIRE", cast=int, default=15 * 60)
JWT_ALGORITHM = config("DEFAULT_TOKEN_EXPIRE",
                       cast=JWTTokenType, default="HS256")
FIRESTORE_PROJECT_ID = config(
    "FIRESTORE_PROJECT_ID", cast=str, default="iitmadrascert"
)
STORAGE_PROJECT_ID = config(
    "FIRESTORE_PROJECT_ID", cast=str, default="iitmadrascert"
)
STORAGE_BUCKET = config(
    "STORAGE_BUCKET", cast=str, default="iitmadrascert.appspot.com"
)