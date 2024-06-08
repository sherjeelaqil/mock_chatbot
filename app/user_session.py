import uuid

class UserSession:
    def __init__(self, websocket):
        self.id = str(uuid.uuid4())
        self.websocket = websocket
