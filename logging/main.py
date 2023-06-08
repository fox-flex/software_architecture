import os
from typing import Dict
import sys
sys.stdout.flush()

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.exceptions import HTTPException
import hazelcast


app = FastAPI()


hz_client = hazelcast.HazelcastClient(
    cluster_name="hz-cluster",
    cluster_members=[
        "hz-1", 
        "hz-2",
        "hz-3"
    ])
db = hz_client.get_map("logging-database").blocking()


@app.on_event("shutdown")
async def shutdown():
    await hz_client.shutdown()

class Message(BaseModel):
    uuid: str
    body: str


@app.get("/")
def get_logs():
    res = ";".join(list(db.values()))
    print(f'GET: returning: "{res}"')
    return res


@app.post("/")
def write_log(msg: Message):
    print(f'POST: recived msg: {msg}')
    db.put(msg.uuid, msg.body)
    return {"message": "LOGGING: Logged successfully!"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}, exc.status_code
