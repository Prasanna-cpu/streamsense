from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from api.events.routing import router as event_router
import os
from contextlib import asynccontextmanager
from api.db.session import init_db

load_dotenv()

port = os.environ["PORT"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix="/api/events", tags=["events"])




@app.get("/")
async def root():
    return {"message": "Hello World !"}


@app.get("/health")
async def health():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port))
