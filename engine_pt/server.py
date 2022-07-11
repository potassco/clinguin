from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from init import init
from server_helper import call_function
from typing import Sequence, Any


class Engine(BaseModel):
    function:str
    arguments:Sequence[str]

(source_files, engines) = init()
app = FastAPI()

@app.post("/")
async def root(engine:Engine):
    result = call_function(engines, engine.function, engine.arguments, {})
    return {"message" : result}


@app.get("/")
async def root2():
    return {"message" : "hello"}



