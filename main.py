from dotenv import load_dotenv
from fastapi import FastAPI
from routers import rag, vector_store

load_dotenv()

app = FastAPI()
app.include_router(rag.router)
app.include_router(vector_store.router)