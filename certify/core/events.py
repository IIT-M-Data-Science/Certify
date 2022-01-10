from typing import Callable
from google.cloud import firestore, storage
from fastapi import FastAPI
from loguru import logger
from certify.core.config import FIRESTORE_PROJECT_ID, STORAGE_PROJECT_ID


def create_start_app_handler(app: FastAPI) -> Callable:
    """FastAPI start app event
    Args:
        app (FastAPI)
    Returns:
        Callable
    """

    @logger.catch
    async def start_app() -> None:
        logger.info("Creating Firebase client")
        db = firestore.AsyncClient(project=FIRESTORE_PROJECT_ID)
        app.state.db = db

        logger.info("Creating Cloud Storage client")
        app.state.storage = storage.Client(project=STORAGE_PROJECT_ID)

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
        logger.info("Disconnecting Firebase client")
        app.state.db.close() # close any open transport

        logger.info("Disconnecting Cloud Storage client")
        app.state.db.close() 

    return stop_app