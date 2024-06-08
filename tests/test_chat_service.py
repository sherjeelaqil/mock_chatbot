import pytest
from app.chat_service import ChatService

@pytest.fixture
def chat_service():
    return ChatService()

def test_start_session(chat_service):
    session_id = chat_service.start_session()
    assert session_id is not None

def test_send_message(chat_service):
    session_id = chat_service.start_session()
    response = chat_service.send_message(session_id, "Hello")
    assert "Mock response" in response

def test_get_history(chat_service):
    session_id = chat_service.start_session()
    chat_service.send_message(session_id, "Hello")
    history = chat_service.get_history(session_id)
    assert len(history) == 1

def test_end_session(chat_service):
    session_id = chat_service.start_session()
    chat_service.end_session(session_id)
    history = chat_service.get_history(session_id)
    assert len(history) == 0
