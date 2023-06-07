import os
from typing import Dict
import random

from uuid import uuid4 as get_uuid
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

try_log_n = 10
logging_urls = os.environ['LOGGING_SERVICE_URLS'].split(",")
message_url = os.environ['MESSAGE_SERVICE_URL']

logging_client = aiohttp.ClientSession()
message_client = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    await logging_client.close()
    await message_client.close()

class Text(BaseModel):
    text: str = ""

@app.post("/", status_code=201)
async def accept_message(text: Text) -> Dict[str, str]:
    msg = text.text
    print(f'received msg: {msg}')

    msg_id = str(get_uuid())
    payload = {"uuid": msg_id, "body": msg}

    for i in range(try_log_n):
        logging_url = random.choice(logging_urls)
        print(f'sending to {logging_url}')
        try:
            async with logging_client.post(logging_url, json=payload) as response:
                response_data = await response.json()
                response.raise_for_status()
                return response_data
        except aiohttp.ClientError as e:
            print(f"POST to logging service attemp #{i}: Error : {e}")
    
    print(f'does not finish logging in {try_log_n} tries')
    raise HTTPException(status_code=500, detail="Error sending message to logging service")


@app.get("/")
async def get_messages() -> str:
    response_data = []

    for i in range(try_log_n):
        logging_url = random.choice(logging_urls)
        try:
            async with logging_client.get(logging_url) as response:
                response_txt = await response.text()
                response_data.append(response_txt[1:-1])
                response.raise_for_status()
                print('GET: {logging_url} success. Response: {response_txt}')
        except aiohttp.ClientError as e:
            print(f"GET from logging service attemp #{i}: Error : {e}")

    try:
        async with message_client.get(message_url) as response:
            response_txt = await response.text()
            response_data.append(response_txt[1:-1])
            response.raise_for_status()
            print('GET: {message_url} success. Response: {response_txt}')
    except aiohttp.ClientError as e:
        print(f"Error retrieving messages from message service: {e}")
    
    return '\n'.join(response_data)
