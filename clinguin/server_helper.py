import uvicorn
from fastapi import FastAPI, APIRouter

from clinguin.utils.logger import Logger
from clinguin.server.presentation.endpoints import Endpoints

def start(args,parse_config, log_dict):

    app = FastAPI()
    
    @app.on_event("startup")
    async def startup_event():
        Logger.setupUvicornLoggerOnStartup(log_dict)

    endpoints = Endpoints(args,parse_config, log_dict)
    app.include_router(endpoints.router)

    uvicorn.run(app)

