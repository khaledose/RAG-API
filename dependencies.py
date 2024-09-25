from services.ChatService import ChatService
from services.DocumentService import DocumentService
from services.SessionService import SessionService
from services.ContextService import ContextService

document_service = DocumentService()
context_service = ContextService()
session_service = SessionService()
chat_service = ChatService(context_service, session_service)

# Dependency for document_service
def get_document_service() -> DocumentService:
    return document_service

# Dependency for ContextService
def get_context_service() -> ContextService:
    return context_service

# Dependency for SessionService
def get_session_service() -> SessionService:
    return session_service

# Dependency for chat_service
def get_chat_service() -> ChatService:
    return chat_service