from typing import Callable

from fastapi import FastAPI
from loguru import logger


def create_start_app_handler(app: FastAPI) -> Callable:
    """FastAPI start app event
    Args:
        app (FastAPI)
    Returns:
        Callable
    """

    async def start_app() -> None:
        logger.info("Connecting to Firebase database")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """FastAPI shutdown event
    Args:
        app (FastAPI)
    Returns:
        Callable
    """

    @logger.catch
    async def stop_app() -> None:
        logger.info("Disconnecting Firebase database")

    return stop_app