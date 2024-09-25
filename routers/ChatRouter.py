from fastapi import APIRouter, Depends
from dependencies import get_chat_service, get_context_service
from schemas.Request import ChatRequest, ContextRequest 
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from services.ContextService import ContextService
from services.ChatService import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/build")
async def chat_build(
    context_request: ContextRequest, 
    context_service: ContextService = Depends(get_context_service),
    chat_service: ChatService = Depends(get_chat_service)):
    context_name = context_request.context_name
    if not context_service.exists(context_name):
            raise HTTPException(status_code=404, detail="Vector store not found.")
    
    try:
        chat_service.build(context_name)
        return {"message": f"Chat with store {context_request.context_name} is ready to use."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build RAG chain: {str(e)}")

@router.post("/")
async def chat(
    chat_request: ChatRequest, 
    context_service: ContextService = Depends(get_context_service),
    chat_service: ChatService = Depends(get_chat_service)):
    context_name = chat_request.context_name
    if not context_service.exists(context_name):
            raise HTTPException(status_code=404, detail="Vector store not found.")
    try:
        return StreamingResponse(chat_service.chat(chat_request.session_id, chat_request.question), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
