import uvicorn
from fastapi import FastAPI, APIRouter

from clinguin.utils.logger import Logger
from clinguin.server.presentation.endpoints import Endpoints


def start(args):

    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        Logger.setupUvicornLoggerOnStartup(args.log_args)

    endpoints = Endpoints(args)
    app.include_router(endpoints.router)

    uvicorn.run(app)
