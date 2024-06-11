from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.chat_service import ChatService
from app.models import MessageRequest, EndSessionRequest


router = APIRouter()
chat_service = ChatService()

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

@router.get("/analytics")
def get_analytics():
    session_data = chat_service.get_session_data()
    message_data = chat_service.get_message_data()

    total_sessions = len(session_data)
    total_messages = len(message_data)
    avg_messages_per_session = total_messages / total_sessions if total_sessions > 0 else 0

    # Calculate average session duration
    total_duration = 0
    for session in session_data:
        if session[2]:  # Check if end_time is not None
            start_time = datetime.fromisoformat(session[1])
            end_time = datetime.fromisoformat(session[2])
            total_duration += (end_time - start_time).total_seconds()

    avg_session_duration = total_duration / total_sessions if total_sessions > 0 else 0

    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "avg_messages_per_session": avg_messages_per_session,
        "avg_session_duration": avg_session_duration
    }