"""context manager for database"""

import aiosqlite


class UseDatabase:

    def __init__(self, dbpath: str):
        self.path = dbpath

    async def __aenter__(self) -> 'cursor':
        self.conn = await aiosqlite.connect(self.path)
        self.cursor = await self.conn.cursor()
        return self.cursor

    async def __aexit__(self, ecx_type, exc_value, exc_trace):
        await self.conn.commit()
        await self.cursor.close()
        await self.conn.close()
