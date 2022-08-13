import sqlite3


class UseDatabase:

    def __init__(self, dbpath: str):
        self.path = dbpath

    def __enter__(self) -> 'cursor':
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, ecx_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
