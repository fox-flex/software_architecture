import os

from fastapi import FastAPI
from starlette.exceptions import HTTPException

app = FastAPI()


@app.get("/")
def get_logs():
    return "Not implemented yet"


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}, exc.status_code
