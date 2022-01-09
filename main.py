import sys
from loguru import logger

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from certify.core.error.http_error import http_error_handler
from certify.core.error.validation_error import http422_error_handler
from certify.routes import router
from certify.core.config import ALLOWED_HOSTS, DEBUG, SECRET_KEY
from certify.core.events import create_start_app_handler, create_stop_app_handler
from certify.core.middleware.jwt import OAuthMiddleware


print(
    """
    ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
    ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
    ██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝ 
    ██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝  
    ╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║   
    ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝   
    """
)

def catch_exceptions():
    sys.excepthook = lambda _type, message, stack: logger.opt(
        exception=(_type, message, stack)
    ).error("Uncaught Exception")

def create_application():
    catch_exceptions()

    app = FastAPI(
        title="Certify", 
        description="Certificate Verfification System API for IITM-POD", 
        version="1.0.0",
        debug=DEBUG
    )

    logger.info(f"Starting Certify CVS server")
    logger.info(f"Island API endpoint - /api/")

    logger.info("Adding middlewares")

    logger.debug("Adding OAuthMiddleware")
    app.add_middleware(OAuthMiddleware)

    logger.debug("Adding CORSMiddleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"], #TODO: Dangerous practise
    )

    logger.info("Adding startup and shutdown events")

    app.add_event_handler(
        "startup", create_start_app_handler(app))
    app.add_event_handler(
        "shutdown", create_stop_app_handler(app))

    logger.info("Adding exception handlers")

    app.add_exception_handler(
        HTTPException, 
        http_error_handler
    )
    app.add_exception_handler(
        RequestValidationError, 
        http422_error_handler
    )

    logger.info("Adding routers")

    app.include_router(router)

    logger.info("Application setup complete")
    
    return app
    

app = create_application()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", log_level="debug")