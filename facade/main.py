import os
from typing import Dict

import uuid
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

logging_service_url = os.environ['LOGGING_SERVICE_URL']
message_service_url = os.environ['MESSAGE_SERVICE_URL']

logging_client = aiohttp.ClientSession()
message_client = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    await logging_client.close()
    await message_client.close()

class Text(BaseModel):
    text: str = ""

@app.post("/", status_code=201)
# async def accept_message(pld: str) -> Dict[str, str]:
async def accept_message(pld: Text) -> Dict[str, str]:
    text = pld.text
    print(f'received msg: {text}')

    msg_id = str(uuid.uuid4())
    payload = {"uuid": msg_id, "body": text}

    try:
        async with logging_client.post(logging_service_url, json=payload) as response:
            response_data = await response.json()
            response.raise_for_status()
            return response_data
    except aiohttp.ClientError as e:
        print(f"Error sending message to logging service: {e}")
    
    raise HTTPException(status_code=500, detail="Error sending message to logging service")


@app.get("/")
async def get_messages() -> str:
    response_data = []

    try:
        async with logging_client.get(logging_service_url) as response:
            response_txt = await response.text()
            response_data.append(response_txt[1:-1])
            print('Logging Service Response:', response.status, response_txt)
            response.raise_for_status()
    except aiohttp.ClientError as e:
        print(f"Error retrieving messages from logging service: {e}")

    try:
        async with message_client.get(message_service_url) as response:
            response_txt = await response.text()
            response_data.append(response_txt[1:-1])
            print('Message Service Response:', response.status, response_txt)
            response.raise_for_status()
    except aiohttp.ClientError as e:
        print(f"Error retrieving messages from message service: {e}")
    
    return '\n'.join(response_data)
