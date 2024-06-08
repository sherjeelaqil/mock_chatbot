from app.user_session import UserSession

class UserManager:
    def __init__(self):
        self.sessions = {}

    def add_session(self, websocket):
        session = UserSession(websocket)
        self.sessions[session.id] = session
        return session

    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session(self, session_id):
        return self.sessions.get(session_id)
