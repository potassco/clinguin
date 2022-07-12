import uvicorn

from server.presentation.endpoints import Endpoints
from fastapi import FastAPI, APIRouter

def startServer(logic_programs, engines):
    app = FastAPI()
    hello = Endpoints(logic_programs, engines, "World")
    app.include_router(hello.router)
    uvicorn.run(app)
