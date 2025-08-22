from dotenv import load_dotenv
from fastapi import FastAPI

import os
import uvicorn


load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok", "message": "Hello World!!!"}


if __name__=="__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))