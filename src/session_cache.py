from cachetools import LRUCache

class SessionCache:
    def __init__(self):
        self.cache = LRUCache(maxsize=1024)

    def get(self, session_id):
        return self.cache.get(session_id, {"messages": []})

    def add(self, session_id, message):
        session_data = self.get(session_id)
        session_data["messages"].append(message)
        self.cache[session_id] = session_data
        
    def is_session_exist(self, session_id):
        return session_id in self.cache
