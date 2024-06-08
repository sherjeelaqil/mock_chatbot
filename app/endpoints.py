from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class MessageRequest(BaseModel):
    session_id: str
    message: str

class EndSessionRequest(BaseModel):
    session_id: str

@router.post("/session/start")
def start_session():
    session_id = chat_service.start_session()
    return {"session_id": session_id}

@router.post("/message")
def send_message(request: MessageRequest):
    try:
        response = chat_service.process_message(request.session_id, request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}/history")
def get_session_history(session_id: str):
    try:
        history = chat_service.get_session_history(session_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/end")
def end_session(request: EndSessionRequest):
    try:
        chat_service.end_session(request.session_id)
        return {"status": "session ended"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
