from dependencies import get_file_service, get_vector_store_service
from services.file import FileService
from services.vector_store import VectorStoreService
from fastapi import File, UploadFile, HTTPException, BackgroundTasks
from schemas.chat import StoreRequest 
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/vector_stores")
async def get_vector_stores(vector_service: VectorStoreService = Depends(get_vector_store_service)):
    try:
        return vector_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vector stores: {str(e)}")

@router.post("/vector_stores")
async def create_vector_store(
    store_request: StoreRequest, 
    vector_service: VectorStoreService = Depends(get_vector_store_service)):
    store_name = store_request.store_name

    if vector_service.exists(store_name):
        raise HTTPException(status_code=400, detail=f"Vector store '{store_name}' already exists.")

    try:
        vector_service.create(store_name)
        return {"message": f"Vector store '{store_name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create vector store: {str(e)}")

@router.post("/vector_stores/{store_name}")
async def update_vector_stores(
    store_name: str, 
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service),
    vector_service: VectorStoreService = Depends(get_vector_store_service)):

    if not vector_service.exists(store_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")

    docs = await file_service.load(file)
    background_tasks.add_task(vector_service.update, docs, store_name)

    return {"message": "File upload initiated. Embeddings will be updated in the background."}

@router.delete("/vector_stores")
async def delete_vector_store(
    store_request: StoreRequest, 
    background_tasks: BackgroundTasks,
    vector_service: VectorStoreService = Depends(get_vector_store_service)):
    
    store_name = store_request.store_name
    if not vector_service.exists(store_name):
        raise HTTPException(status_code=404, detail=f"Vector store '{store_name}' not found.")

    try:
        background_tasks.add_task(vector_service.delete, store_name)
        return {"message": f"Vector store '{store_name}' deletion initiated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vector store: {str(e)}")
