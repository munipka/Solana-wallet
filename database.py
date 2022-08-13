
from SImpleTest import config
from SImpleTest.DBcm import UseDatabase

dbname = config.DATABASE_NAME


def create_table():
    with UseDatabase(dbname) as cursor:
        _SQL = """CREATE TABLE IF NOT EXISTS users(
        user_id INT );
        """
        cursor.execute(_SQL)
        return cursor.fetchall()


def user_check(user_id):
    with UseDatabase(dbname) as cursor:
        _SQL = """SELECT* FROM users WHERE user_id=?"""
        cursor.execute(_SQL, (user_id,))
        res = cursor.fetchone()
        if res is None:
            return False
        else:
            return True


def add_user(user_id):
    with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO users (user_id)
        VAlUES(?);"""
        cursor.execute(_SQL, (user_id,))


def save_history(user_id, address, amount, transaction, date):
    with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO history (user_id, address, amount, trans, date) 
         VALUES(?, ?, ?, ?, ?);"""
        cursor.execute(_SQL, (user_id, address, amount, transaction, date))
        return True


def get_history(user_id):
    with UseDatabase(dbname) as cursor:
        _SQL = """SELECT address, amount, trans FROM history
        WHERE user_id = ?
        ORDER BY date DESC LIMIT 5"""
        cursor.execute(_SQL, (user_id,))
        content = cursor.fetchmany(5)
        return content


def show_smt():
    with UseDatabase(dbname) as cursor:
        _SQL = """SELECT * FROM saved_addresses"""
        cursor.execute(_SQL)
        res = cursor.fetchall()
        print(res)
