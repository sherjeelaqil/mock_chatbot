import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
from app.message_dispatcher import MessageDispatcher
from app.user_manager import UserManager

class WebSocketServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.user_manager = UserManager()
        self.message_dispatcher = MessageDispatcher()

    async def handler(self, websocket, path):
        session = self.user_manager.add_session(websocket)
        try:
            async for message in websocket:
                await self.message_dispatcher.dispatch(session, message)
        except ConnectionClosedError:
            pass
        finally:
            self.user_manager.remove_session(session.id)

    def start(self):
        loop = asyncio.get_event_loop()
        server = websockets.serve(self.handler, self.host, self.port)
        loop.run_until_complete(server)
        loop.run_forever()

if __name__ == "__main__":
    server = WebSocketServer()
    server.start()
