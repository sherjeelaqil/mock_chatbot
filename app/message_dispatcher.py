import json
from app.chat_service import ChatService
from app.third_party import ThirdPartyService

class MessageDispatcher:
    def __init__(self):
        self.chat_service = ChatService()

    async def dispatch(self, session, message, third_party_service: ThirdPartyService):
        session_id = session.id
        message_data = json.loads(message)
        enriched_response = third_party_service.get_weather()
        response = self.chat_service.process_message(session_id, message_data["message"])
        # Return a JSON-encoded response string
        return json.dumps({"response": response, "Weather": enriched_response})