import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret, URL

from certify.core.logging import InterceptHandler 
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

logging.getLogger().handlers = [InterceptHandler()]
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.setLevel(logging.INFO)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]