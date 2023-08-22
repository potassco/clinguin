"""
Responsible for starting the server
"""
import uvicorn
from fastapi import FastAPI

from clinguin.server import Endpoints
from clinguin.utils import Logger


def start(args):
    """
    Function that starts the uvicorn server.
    """

    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        Logger.setup_uvicorn_logger_on_startup(args.log_args)

    endpoints = Endpoints(args)
    app.include_router(endpoints.router)

    uvicorn.run(app)
