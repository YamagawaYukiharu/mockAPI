from fastapi import FastAPI
import configparser
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

# Root endpoint to check the API
@app.get("/")
def read_root():
    return {"message": "MockPIE is working! Check /info to more information..."}


# Endpoint to check some info
@app.get("/info")
def read_root():
    return {"message": "This is a test version, soon there will be more...."}
