from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.agent import chat

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat_api(request: ChatRequest):
    return chat([m.dict() for m in request.messages])