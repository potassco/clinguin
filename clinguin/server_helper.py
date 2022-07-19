import uvicorn
import logging

from .server.presentation.endpoints import Endpoints
from fastapi import FastAPI, APIRouter

def start(logic_programs, engines, time_stamp):
    log_file_name = time_stamp + "-server"
    app = FastAPI()
    

    @app.on_event("startup")
    async def startup_event():
        log_file_path = "./logs/" + log_file_name + ".log"
        formatter = logging.Formatter('%(levelname)s<%(asctime)s>: %(message)s')

        logger = logging.getLogger("uvicorn.access")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logger = logging.getLogger("uvicorn.error")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logger = logging.getLogger("uvicorn")
        for handler in logger.handlers:
            logger.removeHandler(handler)

        handler_f = logging.FileHandler(log_file_path)
        handler_f.setFormatter(formatter)
        handler_sh = logging.StreamHandler()
        handler_sh.setFormatter(formatter)

        logger.addHandler(handler_f)
        logger.addHandler(handler_sh)


    hello = Endpoints(logic_programs, engines, log_file_name)
    app.include_router(hello.router)

    uvicorn.run(app)

