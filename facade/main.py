import os
from typing import Dict

import uuid
import aiohttp
from fastapi import FastAPI, HTTPException
from aiohttp.client_exceptions import ContentTypeError


app = FastAPI()

logging_service_url = os.environ['LOGGING_SERVICE_URL']
message_service_url = os.environ['MESSAGE_SERVICE_URL']

logging_client = aiohttp.ClientSession()
message_client = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    await logging_client.close()
    await message_client.close()


@app.post("/")
async def accept_message(msg: str) -> Dict[str, str]:
    msg_id = str(uuid.uuid4())
    payload = {"uuid": msg_id, "msg": msg}

    async with logging_client.post(logging_service_url, json=payload) as response:
        response_data = await response.json()
        response.raise_for_status()

    return response_data


@app.get("/")
async def get_messages() -> str:
    response_data = []

    async with logging_client.get(logging_service_url) as response:
        response_txt = await response.text()
        response_data.append(response_txt[1:-1])
        print('Logging Service Response:', response.status, response_txt)
        response.raise_for_status()

    async with message_client.get(message_service_url) as response:
        response_txt = await response.text()
        response_data.append(response_txt[1:-1])
        print('Message Service Response:', response.status, response_txt)
        response.raise_for_status()
    return '\n'.join(response_data)
