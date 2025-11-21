from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from agent.orchestrator import Orchestrator
from watcher import Watcher

load_dotenv()

# Global instances
orchestrator = Orchestrator()
watcher = Watcher(watch_dir=os.path.abspath("../drop_zone"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    watcher.start()
    yield
    # Shutdown
    watcher.stop()

app = FastAPI(title="Remote Coding Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Remote Coding Assistant Backend is Running"}

@app.post("/agent/ask")
async def ask_agent(request: str):
    response = await orchestrator.process_request(request)
    return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now, later connect to agent events
            await websocket.send_text(f"Received: {data}")
            
            # Simulate agent processing
            response = await orchestrator.process_request(data)
            await websocket.send_text(f"Agent: {response}")
            
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
