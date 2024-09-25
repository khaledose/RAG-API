from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session_service
from services.SessionService import SessionService
from uuid import UUID

router = APIRouter(prefix="/sessions", tags=["Session"])

@router.get("/")
async def get_all_sessions(
    session_service: SessionService = Depends(get_session_service)):
    """Get all active session IDs."""
    return session_service.get_all()

@router.get("/{session_id}")
async def get_session(
    session_id: UUID, 
    session_service: SessionService = Depends(get_session_service)
):
    """Retrieve the chat history for a specific session."""
    session = session_service.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
    return session

@router.post("/")
async def create_session(
    session_service: SessionService = Depends(get_session_service)):
    """Create a new session and return its ID."""
    try:
        return session_service.new()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.delete("/{session_id}")
async def delete_session(
    session_id: UUID, 
    session_service: SessionService = Depends(get_session_service)
):
    """Delete a session by session ID."""
    if not session_service.delete(session_id):
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
    return {"detail": f"Session {session_id} deleted successfully."}

@router.delete("/")
async def clear_sessions(
    session_service: SessionService = Depends(get_session_service)):
    """Clear all active sessions."""
    session_service.clear()
    return {"detail": "All sessions cleared."}
