import aiosqlite
from fastapi import APIRouter, Depends
from ..database import get_db_conn

router = APIRouter()

@router.get("/tracks")
async def tracks(connection: aiosqlite.Connection = Depends(get_db_conn)):
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute("SELECT Name FROM tracks")
    data = await cursor.fetchall()
    return data