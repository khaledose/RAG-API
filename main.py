from dotenv import load_dotenv
from fastapi import FastAPI
from routers import chat, vector_store, session

load_dotenv()

app = FastAPI()
app.include_router(vector_store.router)
app.include_router(session.router)
app.include_router(chat.router)