from utils.files import create_temp_dir
from services.vector_store import VectorStoreService
from fastapi import File, UploadFile, HTTPException, BackgroundTasks
from schemas.chat import StoreRequest 
from fastapi import APIRouter, Depends
from dependencies import get_vector_store_service

router = APIRouter()

@router.get("/vector_stores")
async def get_vector_stores(vectorService: VectorStoreService = Depends(get_vector_store_service)):
    try:
        stores = vectorService.get_all()
        return {"vector_stores": stores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vector stores: {str(e)}")

@router.post("/vector_stores")
async def create_vector_store(
    store_request: StoreRequest, 
    vectorService: VectorStoreService = Depends(get_vector_store_service)):
    store_name = store_request.store_name

    if vectorService.exists(store_name):
        raise HTTPException(status_code=400, detail=f"Vector store '{store_name}' already exists.")

    try:
        vectorService.create(store_name)
        return {"message": f"Vector store '{store_name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create vector store: {str(e)}")

@router.post("/vector_stores/{store_name}/{file_type}")
async def update_vector_stores(
    store_name: str, 
    file_type: str, 
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    vectorService: VectorStoreService = Depends(get_vector_store_service)):
    if not vectorService.exists(store_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")
    temp_file = create_temp_dir(file)
    background_tasks.add_task(vectorService.update, temp_file, store_name, file_type)
    return {"message": "File upload initiated. Embeddings will be updated in the background."}

@router.delete("/vector_stores")
async def delete_vector_store(
    store_request: StoreRequest, 
    vectorService: VectorStoreService = Depends(get_vector_store_service)):
    store_name = store_request.store_name

    if not vectorService.exists(store_name):
        raise HTTPException(status_code=404, detail="Vector store not found.")
    
    try:
        vectorService.delete(store_name)
        return {"message": f"Vector store '{store_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vector store: {str(e)}")
