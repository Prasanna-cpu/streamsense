from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

port = os.environ["PORT"]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World !"}


@app.get("/health")
async def health():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port))
