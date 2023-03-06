import os
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.exceptions import HTTPException

app = FastAPI()
logging_map: Dict[str, str] = {}


class Message(BaseModel):
    uuid: str
    body: str


@app.get("/")
def get_logs():
    return ";".join(logging_map.values())


@app.post("/")
def write_log(message: Message):
    logging_map[message.uuid] = message.body
    return {"message": "Logged successfully!"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}, exc.status_code
