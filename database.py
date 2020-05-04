import aiosqlite

SQL_DATABASE_ADDRESS = ".\\databases\\chinook.db"
# database connection is set up by startup event
DATABASE_CONNECTION: aiosqlite.Connection = None

async def get_db_conn():
    return DATABASE_CONNECTION