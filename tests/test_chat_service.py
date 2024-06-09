import pathlib
import pytest
import sys
sys.path.append(str(pathlib.Path().resolve()))
from app.chat_service import ChatService

@pytest.fixture
def chat_service():
    return ChatService()

def test_start_session(chat_service):
    session_id = chat_service.start_session()
    assert session_id is not None

def test_send_message(chat_service):
    session_id = chat_service.start_session()
    response = chat_service.process_message(session_id, "Hello")
    assert "Response :" in response

def test_get_history(chat_service):
    session_id = chat_service.start_session()
    chat_service.process_message(session_id, "Hello")
    history = chat_service.get_session_history(session_id)
    assert len(history) == 1

def test_end_session(chat_service):
    session_id = chat_service.start_session()
    chat_service.end_session(session_id)
    history = chat_service.get_session_history(session_id)
    assert len(history) == 0
