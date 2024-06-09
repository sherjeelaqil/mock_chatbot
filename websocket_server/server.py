import asyncio
import json
import pathlib
import websockets
import sys
sys.path.append(str(pathlib.Path().resolve()))
from app.message_dispatcher import MessageDispatcher
from app.user_manager import UserManager
from websockets.exceptions import ConnectionClosedError

class WebSocketServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.user_manager = UserManager()
        self.message_dispatcher = MessageDispatcher()

    async def handler(self, websocket, path):
        session = self.user_manager.add_session(websocket)
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                response = await self.message_dispatcher.dispatch(session, message)
                print(f"Dispatch response: {response}")
                await websocket.send(response)
        except ConnectionClosedError:
            pass
        finally:
            self.user_manager.remove_session(session.id)

    def start(self):
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = websockets.serve(self.handler, self.host, self.port)
        loop.run_until_complete(server)
        loop.run_forever()

if __name__ == "__main__":
    server = WebSocketServer()
    server.start()
