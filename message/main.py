import os
import json
import threading
import sys
sys.stdout.flush()

from fastapi import FastAPI
from starlette.exceptions import HTTPException

from kafka import KafkaConsumer



class MessageDataBase:
    kafka_url = os.environ['KAFKA_SERVER_URL']
    kafka_topic = os.environ['KAFKA_TOPIC']

    consumer = KafkaConsumer(
        kafka_topic,
        group_id            = 'my-group',
        bootstrap_servers   = [kafka_url],
        auto_offset_reset   = 'earliest',
        enable_auto_commit  = True,
        api_version=(2,0,2),
    )

    db = []
    
    @staticmethod
    def get_all():
        return MessageDataBase.db
    
    @staticmethod
    def consume_loop():
        for msg in MessageDataBase.consumer:
            msg = msg.value.decode()
            print(f"MESSAGE: MessageDataBase: adding msg: {msg}")
            MessageDataBase.db.append(msg)
    
    @staticmethod
    def consume_stop():
        MessageDataBase.consumer.stop()


app = FastAPI()

@app.get("/")
def get_logs():
    res =  ';'.join(MessageDataBase.get_all())
    print(f'MESSAGE: GET: returning: "{res}"')
    return res

@app.on_event("startup")
def startup_event():
    print(f"MESSAGE: startup: start listening on mq")
    t = threading.Thread(target=MessageDataBase.consume_loop)
    t.start()

@app.on_event("shutdown")
def shutdown():
    print(f"MESSAGE: shutdown: stop listening on mq")
    MessageDataBase.consume_stop()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}, exc.status_code
