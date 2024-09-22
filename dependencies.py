from services.rag import RAGService
from services.vector_store import VectorStoreService

vectorService = VectorStoreService()
ragService = RAGService(vectorService)

# Dependency for VectorStoreService
def get_vector_store_service():
    return vectorService

# Dependency for RAGService
def get_rag_service():
    return ragService