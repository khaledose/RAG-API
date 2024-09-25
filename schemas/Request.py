from uuid import UUID
from pydantic import BaseModel

class ContextRequest(BaseModel):
    context_name: str

class ChatRequest(BaseModel):
    session_id: UUID
    context_name: str
    question: str