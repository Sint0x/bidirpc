from aiocache import Cache
from aiocache.serializers import JsonSerializer


class SessionCache:
    def __init__(self):
        self.cache = Cache(Cache.MEMORY, serializer=JsonSerializer(), namespace="main")

    async def get(self, session_id):
        session_data = await self.cache.get(session_id)
        if session_data is None:
            return {"messages": []}
        return session_data

    async def add(self, session_id, message):
        session_data = await self.get(session_id)
        session_data["messages"].append(message)
        await self.cache.set(session_id, session_data)
        
    async def is_session_exist(self, session_id):
        session_data = await self.cache.get(session_id)
        return not not session_data
