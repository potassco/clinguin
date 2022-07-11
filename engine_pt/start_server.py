import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from init import init

if __name__ == '__main__':
    init()
    uvicorn.run('server:app', port=8000, reload=True)


