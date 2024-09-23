from fastapi import APIRouter, Depends
from dependencies import get_chat_service, get_vector_store_service
from schemas.chat import ChatRequest, StoreRequest 
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from services.vector_store import VectorStoreService
from services.chat import ChatService

router = APIRouter()

@router.post("/chat/build")
async def chat_build(
    store_request: StoreRequest, 
    vector_service: VectorStoreService = Depends(get_vector_store_service),
    chat_service: ChatService = Depends(get_chat_service)):
    store_name = store_request.store_name
    if not vector_service.exists(store_name):
            raise HTTPException(status_code=404, detail="Vector store not found.")
    
    try:
        chat_service.build(store_name)
        return {"message": f"Chat with store {store_request.store_name} is ready to use."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build RAG chain: {str(e)}")

@router.post("/chat")
async def chat(
    chat_request: ChatRequest, 
    vector_service: VectorStoreService = Depends(get_vector_store_service),
    chat_service: ChatService = Depends(get_chat_service)):
    store_name = chat_request.store_name
    if not vector_service.exists(store_name):
            raise HTTPException(status_code=404, detail="Vector store not found.")
    try:
        return StreamingResponse(chat_service.chat(chat_request.session_id, chat_request.question), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
