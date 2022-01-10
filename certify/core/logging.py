import logging
from types import FrameType
from typing import cast
from loguru import logger
from certify.core.config import LOGGING_LEVEL

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info, colors=True).log(
            level,
            record.getMessage(),
        )
        

def intercept_logging():
    logging.getLogger().handlers = [InterceptHandler()]
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.setLevel(logging.INFO)
        logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]