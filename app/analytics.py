import time
from collections import defaultdict
from functools import lru_cache

class Analytics:
    def __init__(self):
        self.active_users = set()
        self.message_count = defaultdict(int)
        self.session_durations = defaultdict(list)

    def user_connected(self, session_id):
        self.active_users.add(session_id)

    def user_disconnected(self, session_id, start_time):
        self.active_users.discard(session_id)
        duration = time.time() - start_time
        self.session_durations[session_id].append(duration)

    def message_sent(self, session_id):
        self.message_count[session_id] += 1
    @lru_cache(maxsize=128)
    def get_statistics(self):
        total_sessions = len(self.message_count)
        total_messages = sum(self.message_count.values())
        avg_messages_per_session = total_messages / total_sessions if total_sessions > 0 else 0
        avg_session_duration = sum([sum(durations) for durations in self.session_durations.values()]) / total_sessions if total_sessions > 0 else 0

        return {
            "active_users": len(self.active_users),
            "total_messages": total_messages,
            "avg_messages_per_session": avg_messages_per_session,
            "avg_session_duration": avg_session_duration
        }
