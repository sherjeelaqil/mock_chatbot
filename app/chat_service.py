import sqlite3
import uuid
from datetime import datetime
from app.chat_model import ChatModel
from functools import lru_cache


class ChatService:
    def __init__(self, db_path='chat.db'):
        self.db_path = db_path
        self.chat_model = ChatModel()
        self._register_datetime_adapter_and_converter()

    def _register_datetime_adapter_and_converter(self):
        """Registers the datetime adapter and converter for SQLite."""

        # Adapter function to convert datetime objects to string
        def adapt_datetime(dt):
            return dt.isoformat()

        # Converter function to convert string to datetime objects
        def convert_datetime(s):
            return datetime.fromisoformat(s.decode('utf-8'))

        # Register the adapter and converter
        sqlite3.register_adapter(datetime, adapt_datetime)
        sqlite3.register_converter("DATETIME", convert_datetime)

    def _connect(self):
        """Connects to the SQLite database with datetime type detection."""
        return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def start_session(self):
        session_id = str(uuid.uuid4())
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (id, created_at) VALUES (?, ?)", (session_id, datetime.now()))
        conn.commit()
        conn.close()
        return session_id

    def end_session(self, session_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    @lru_cache(maxsize=128)
    def process_message(self, session_id, message):
        response = self.chat_model.generate_response(message)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (session_id, message, response, timestamp) VALUES (?, ?, ?, ?)",
                       (session_id, message, response, datetime.now()))
        conn.commit()
        conn.close()
        return response

    @lru_cache(maxsize=128)
    def get_session_history(self, session_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT message, response, timestamp FROM messages WHERE session_id = ?", (session_id,))
        history = cursor.fetchall()
        conn.close()
        return [{"message": row[0], "response": row[1], "timestamp": row[2]} for row in history]

    def get_session_data(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, created_at, end_time FROM sessions''')
        history = cursor.fetchall()
        conn.close()
        return history

    def get_message_data(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, message, timestamp FROM messages''')
        history = cursor.fetchall()
        conn.close()
        return history