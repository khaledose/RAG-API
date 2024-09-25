from dependencies import get_document_service, get_context_service
from services.DocumentService import DocumentService
from services.ContextService import ContextService
from fastapi import File, UploadFile, HTTPException, BackgroundTasks
from schemas.Request import ContextRequest 
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/contexts", tags=["Context"])

@router.get("/")
async def get_all_contexts(
    context_service: ContextService = Depends(get_context_service)):
    try:
        return context_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vector stores: {str(e)}")

@router.post("/")
async def create_context(
    context_request: ContextRequest, 
    context_service: ContextService = Depends(get_context_service)):
    context_name = context_request.context_name

    if context_service.exists(context_name):
        raise HTTPException(status_code=400, detail=f"Vector store '{context_name}' already exists.")

    try:
        context_service.create(context_name)
        return {"message": f"Vector store '{context_name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create vector store: {str(e)}")

@router.post("/{context_name}/file/")
async def add_file_to_context(
    context_name: str, 
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
    context_service: ContextService = Depends(get_context_service)):

    if not context_service.exists(context_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")

    docs = await document_service.load_file(file)
    background_tasks.add_task(context_service.update, docs, context_name)

    return {"message": "File upload initiated. Embeddings will be updated in the background."}

@router.post("/{context_name}/web/")
async def add_webpage_to_context(
    context_name: str, 
    url: str,
    background_tasks: BackgroundTasks, 
    document_service: DocumentService = Depends(get_document_service),
    context_service: ContextService = Depends(get_context_service)):

    if not context_service.exists(context_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")

    docs = await document_service.load_web(url)
    background_tasks.add_task(context_service.update, docs, context_name)

    return {"message": "Web page sent. Embeddings will be updated in the background."}

@router.delete("/{context_name}/")
async def delete_context(
    context_name: str, 
    background_tasks: BackgroundTasks,
    context_service: ContextService = Depends(get_context_service)):
    if not context_service.exists(context_name):
        raise HTTPException(status_code=404, detail=f"Vector store '{context_name}' not found.")

    try:
        background_tasks.add_task(context_service.delete, context_name)
        return {"message": f"Vector store '{context_name}' deletion initiated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vector store: {str(e)}")
