"""
Responsible for starting the server
"""
import uvicorn
from fastapi import FastAPI

from clinguin.utils import Logger
from clinguin.server import Endpoints
from starlette.middleware.cors import CORSMiddleware

def start(args):
    """
    Function that starts the uvicorn server.
    """

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    @app.on_event("startup")
    async def startupEvent():
        Logger.setup_uvicorn_logger_on_startup(args.log_args)

    endpoints = Endpoints(args)
    app.include_router(endpoints.router)

    uvicorn.run(app)
