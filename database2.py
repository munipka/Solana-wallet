import config
import asyncio
from DBcm import UseDatabase

#dbname = config.DATABASE_NAME
dbname = 'database/test.db'

async def create_table():
    async with UseDatabase(dbname) as cursor:
        _SQL = """CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER 
        );
        """
        await cursor.execute(_SQL)
        
        _SQL="""CREATE TABLE IF NOT EXISTS addresses(
        user_id INTEGER,
        address TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
        await cursor.execute(_SQL)
        
        _SQL="""CREATE TABLE IF NOT EXISTS history(
        user_id INTEGER,
        address TEXT,
        amount FLOAT,
        trans  TEXT,
        date INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        );        
        """
        await cursor.execute(_SQL)
        
        _SQL = """CREATE TABLE IF NOT EXISTS wallets(
        user_id INTEGER,
        public TEXT,
        secret BLOB,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (public) REFERENCES addresses(address)
        );
        """
        await cursor.execute(_SQL)

async def save_wallet_keys(user_id, public, secret):
    async with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO wallets (user_id, public, secret)
        VALUES(?, ?, ?);"""
        await cursor.execute(_SQL, (user_id, public, secret))
        
        
async def load_wallet_keys(user_id):
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT secret FROM wallets 
        WHERE user_id =?; """
        await cursor.execute(_SQL, (user_id,))
        res = await cursor.fetchone()
        return res
              

async def user_check(user_id):
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT* FROM users WHERE user_id=?;"""
        await cursor.execute(_SQL, (user_id,))
        res = await cursor.fetchone()
        if res is None:
            return False
        else:
            return True

async def add_user(user_id):
    async with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO users (user_id)
        VAlUES (?);"""
        await cursor.execute(_SQL, (user_id,)) 


async def save_history(user_id, address, amount, transaction, date):
    async with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO history (user_id, address, amount, trans, date) 
         VALUES(?, ?, ?, ?, ?);"""
        await cursor.execute(_SQL, (user_id, address, amount, transaction, date))
        return True


async def get_history(user_id):
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT address, amount, trans FROM history
        WHERE user_id = ?
        ORDER BY date DESC LIMIT 5"""
        await cursor.execute(_SQL, (user_id,))
        content = await cursor.fetchmany(5)
        return content

async def save_address(user_id, address):
    async with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO addresses (user_id, address)
        VALUES(?, ?);"""
        await cursor.execute(_SQL, (user_id, address))

        
async def select_address(user_id):
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT address FROM addresses
        WHERE user_id=?;"""
        await cursor.execute(_SQL, (user_id,))
        res = await cursor.fetchone()
        return res
        
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_table())