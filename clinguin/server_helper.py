"""
Responsible for starting the server
"""
import uvicorn
from fastapi import FastAPI

from clinguin.utils import Logger
from clinguin.server import Endpoints


def start(args):
    """
    Function that starts the uvicorn server.
    """

    app = FastAPI()

    @app.on_event("startup")
    async def startupEvent():
        Logger.setupUvicornLoggerOnStartup(args.log_args)

    endpoints = Endpoints(args)
    app.include_router(endpoints.router)

    uvicorn.run(app)
