import sqlite3
import uuid
from datetime import datetime
from app.chat_model import ChatModel

class ChatService:
    def __init__(self, db_path='chat.db'):
        self.db_path = db_path
        self.chat_model = ChatModel()

    def start_session(self):
        session_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (id, created_at) VALUES (?, ?)", (session_id, datetime.now()))
        conn.commit()
        conn.close()
        return session_id

    def end_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    def process_message(self, session_id, message):
        response = self.chat_model.generate_response(message)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (session_id, message, response, timestamp) VALUES (?, ?, ?, ?)",
                       (session_id, message, response, datetime.now()))
        conn.commit()
        conn.close()
        return response

    def get_session_history(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT message, response, timestamp FROM messages WHERE session_id = ?", (session_id,))
        history = cursor.fetchall()
        conn.close()
        return [{"message": row[0], "response": row[1], "timestamp": row[2]} for row in history]
