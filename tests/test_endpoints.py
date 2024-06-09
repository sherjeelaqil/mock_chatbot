from fastapi.testclient import TestClient
import pathlib
import sys
sys.path.append(str(pathlib.Path().resolve()))
from app.main import app

client = TestClient(app)

def test_start_session():
    response = client.post("/session/start")
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_send_message():
    session_id = client.post("/session/start").json()["session_id"]
    response = client.post("/message", json={"session_id": session_id, "message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_get_history():
    session_id = client.post("/session/start").json()["session_id"]
    client.post("/message", json={"session_id": session_id, "message": "Hello"})
    response = client.get(f"/session/{session_id}/history")
    assert response.status_code == 200
    assert len(response.json()["history"]) == 1

def test_end_session():
    session_id = client.post("/session/start").json()["session_id"]
    response = client.post("/session/end", json={"session_id": session_id})
    assert response.status_code == 200
    history_response = client.get(f"/session/{session_id}/history")
    assert len(history_response.json()["history"]) == 0
