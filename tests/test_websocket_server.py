import asyncio
import websockets
import json
import pytest

@pytest.mark.asyncio
async def test_websocket():
    async with websockets.connect("ws://localhost:8080") as websocket:
        await websocket.send(json.dumps({"session_id": "test", "message": "Hello"}))
        response = await websocket.recv()
        assert "Response :" in json.loads(response)["response"]
