import uvicorn

from clinguin.utils.logger import Logger

from clinguin.server.presentation.endpoints import Endpoints
from fastapi import FastAPI, APIRouter

def start(args_dict, parsed_config):

    app = FastAPI()
    
    @app.on_event("startup")
    async def startup_event():
        Logger.setupUvicornLoggerOnStartup(parsed_config['logger']['server'])

    endpoints = Endpoints(args_dict, parsed_config)
    app.include_router(endpoints.router)

    uvicorn.run(app)

