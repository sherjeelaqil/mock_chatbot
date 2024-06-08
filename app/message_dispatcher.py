from app.chat_service import ChatService

class MessageDispatcher:
    def __init__(self):
        self.chat_service = ChatService()

    async def dispatch(self, session, message):
        session_id = session.id
        response = self.chat_service.process_message(session_id, message)
        await session.websocket.send(response)
