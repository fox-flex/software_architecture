import os
from typing import Dict
import random
import hashlib
import json
import sys
sys.stdout.flush()

from uuid import uuid4 as get_uuid
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer, KafkaAdminClient, KafkaClient
from kafka.admin import NewPartitions
from kafka.errors import KafkaError
from kafka.partitioner import DefaultPartitioner


app = FastAPI()

try_n = 10
logging_urls = os.environ['LOGGING_SERVICE_URLS'].split(",")
message_urls = os.environ['MESSAGE_SERVICE_URLS'].split(",")
kafka_url = os.environ['KAFKA_SERVER_URL']
kafka_topic = os.environ['KAFKA_TOPIC']


logging_client = aiohttp.ClientSession()
message_client = aiohttp.ClientSession()


producer = KafkaProducer(
    bootstrap_servers = [kafka_url],
    value_serializer  = lambda x: str.encode(x),
    api_version=(2,0,2),
)

if len(producer.partitions_for(kafka_topic)) < len(message_urls):
    print('facade: Increassing number of partitions to allow parallelisation for consumer')
    admin_client = KafkaAdminClient(bootstrap_servers = [kafka_url], api_version=(2,0,2))
    partitions = {}
    partitions[kafka_topic] = NewPartitions(total_count = len(message_urls))
    admin_client.create_partitions(partitions)
    print('facade: Increassing number of partitions: done')

@app.on_event("startup")
def startup_event():
    print(f"facade: startup: started successfully")

@app.on_event("shutdown")
async def shutdown():
    await logging_client.close()
    await message_client.close()


class Text(BaseModel):
    text: str = ""


@app.post("/", status_code=201)
async def accept_message(text: Text) -> Dict[str, str]:
    msg = text.text
    print(f'facade: POST: received msg: {msg}')

    msg_id = str(get_uuid())
    payload = {"uuid": msg_id, "body": msg}

    # post to logging services
    for i in range(try_n):
        logging_url = random.choice(logging_urls)
        print(f'facade: POST: sending to {logging_url}')
        try:
            async with logging_client.post(logging_url, json=payload) as response:
                response_data = await response.json()
                response.raise_for_status()
                # return response_data
            break
        except aiohttp.ClientError as e:
            print(f"facade: POST: to logging service attemp #{i}: Error : {e}")
    else:
        print(f'facade: POST: does not finish logging in {try_n} tries')
        raise HTTPException(status_code=500, detail="Error sending message to logging service")
    print(f'facade: POST: sending to {logging_url}: success')

    # post to messege services via mq
    print(f"facade: POST: to messege service by mq, msg: {msg}")
    future = producer.send(kafka_topic, value=msg)
    try:
        record_metadata = future.get(timeout=10)
        print(f'facade: POST: mq.topic     : {record_metadata.topic}')
        print(f'facade: POST: mq.partition : {record_metadata.partition}')
        print(f'facade: POST: mq.offset    : {record_metadata.offset}')
        # print(f'facade: POST: mq responce: {record_metadata}')
    except KafkaError as err:
        print(f'facade: POST: mq kafkaError: {err}')
    print(f"facade: POST: to messege service by mq: done")
    
    return 'OK'


@app.get("/")
async def get_messages() -> str:
    response_data = []

    # get from logging services
    for i in range(try_n):
        logging_url = random.choice(logging_urls)
        try:
            async with logging_client.get(logging_url) as response:
                response_txt = await response.text()
                response_data.append(response_txt[1:-1])
                response.raise_for_status()
                print(f'facade: GET: {logging_url} success. Response: "{response_txt}"')
                break
        except aiohttp.ClientError as e:
            print(f"facade: GET from logging service attemp #{i}: Error : {e}")

    # get from messege services
    for i in range(try_n):
        message_url = random.choice(message_urls)
        try:
            async with message_client.get(message_url) as response:
                response_txt = await response.text()
                response_data.append(response_txt[1:-1])
                response.raise_for_status()
                print(f'facade: GET: {message_url} success. Response: "{response_txt}"')
                break
        except aiohttp.ClientError as e:
            print(f'facade: GET: Error retrieving messages from message service: {e}')

    return '\n'.join(response_data)
