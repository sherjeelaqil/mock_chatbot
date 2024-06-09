import json
from app.chat_service import ChatService

class MessageDispatcher:
    def __init__(self):
        self.chat_service = ChatService()

    async def dispatch(self, session, message):
        session_id = session.id
        message_data = json.loads(message)
        response = self.chat_service.process_message(session_id, message_data["message"])
        # Return a JSON-encoded response string
        return json.dumps({"response": response})