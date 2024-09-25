from dotenv import load_dotenv
from fastapi import FastAPI
from routers import ChatRouter, ContextRouter, SessionRouter

load_dotenv()

app = FastAPI()
app.include_router(ContextRouter.router)
app.include_router(SessionRouter.router)
app.include_router(ChatRouter.router)