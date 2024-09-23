from services.chat import ChatService
from services.file import FileService
from services.session import SessionService
from services.vector_store import VectorStoreService

file_service = FileService()
vector_service = VectorStoreService()
session_service = SessionService()
chat_service = ChatService(vector_service, session_service)

# Dependency for file_service
def get_file_service() -> FileService:
    return file_service

# Dependency for VectorStoreService
def get_vector_store_service() -> VectorStoreService:
    return vector_service

# Dependency for SessionService
def get_session_service() -> SessionService:
    return session_service

# Dependency for chat_service
def get_chat_service() -> ChatService:
    return chat_service