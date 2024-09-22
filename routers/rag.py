from fastapi import APIRouter, Depends
from schemas.chat import ChatRequest, StoreRequest 
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from services.vector_store import VectorStoreService
from services.rag import RAGService
from dependencies import get_vector_store_service, get_rag_service

router = APIRouter()

@router.post("/rag/build")
async def build_rag(
    store_request: StoreRequest, 
    vectorService: VectorStoreService = Depends(get_vector_store_service),
    ragService: RAGService = Depends(get_rag_service)):
    store_name = store_request.store_name

    if not vectorService.exists(store_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")

    try:
        ragService.build(store_name)
        return {"message": f"RAG chain with vector store '{store_name}' built successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build RAG chain: {str(e)}")

@router.post("/rag/chat")
async def chat_rag(chat_request: ChatRequest, 
    vectorService: VectorStoreService = Depends(get_vector_store_service),
    ragService: RAGService = Depends(get_rag_service)):
    try:
        if not vectorService.exists(chat_request.store_name):
            raise HTTPException(status_code=404, detail="Vector store not found.")
        
        return StreamingResponse(ragService.chat(chat_request.session_id, chat_request.question), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
