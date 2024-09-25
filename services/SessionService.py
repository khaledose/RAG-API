import uuid
from uuid import UUID
from typing import Dict, List, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

class SessionService:
    def __init__(self):
        self.sessions: Dict[UUID, BaseChatMessageHistory] = {}
    
    def get_all(self) -> List[UUID]:
        """Return a list of all session IDs."""
        return list(self.sessions.keys())

    def get(self, session_id: UUID) -> BaseChatMessageHistory:
        """Return the chat history for a specific session or None if not found."""
        return self.sessions[session_id]

    def new(self) -> UUID:
        """Create a new session and return its session ID."""
        session_id = uuid.uuid4()
        self.sessions[session_id] = ChatMessageHistory()
        return session_id

    def delete(self, session_id: UUID) -> bool:
        """Delete a session. Return True if session was deleted, False if it was not found."""
        return self.sessions.pop(session_id, None) is not None

    def clear(self) -> None:
        """Clear all sessions."""
        self.sessions.clear()
