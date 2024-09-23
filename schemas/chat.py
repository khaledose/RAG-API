from uuid import UUID
from pydantic import BaseModel

class StoreRequest(BaseModel):
    store_name: str

class ChatRequest(BaseModel):
    session_id: UUID
    store_name: str
    question: str