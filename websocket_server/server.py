import asyncio
import websockets
import json
import uuid
import pathlib
import sys
sys.path.append(str(pathlib.Path().resolve()))
from app.message_dispatcher import MessageDispatcher
from app.user_manager import UserManager
from app.chat_service import ChatService
from app.analytics import Analytics
# from app.third_party import ThirdPartyService
import time

class WebSocketServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.user_manager = UserManager()
        self.chat_service = ChatService()
        self.message_dispatcher = MessageDispatcher()#self.chat_service, ThirdPartyService()
        self.analytics = Analytics()

    async def handler(self, websocket, path):
        session_id = str(uuid.uuid4())
        session = self.user_manager.add_session(websocket)
        self.analytics.user_connected(session_id)

        try:
            async for message in websocket:
                response = await self.message_dispatcher.dispatch(session, message)
                await websocket.send(json.dumps({"response": response}))

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        finally:
            self.chat_service.end_session(session_id)
            self.user_manager.remove_session(session_id)

    def run(self):
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        start_server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = WebSocketServer()
    server.run()
