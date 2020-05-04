from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict
from database import get_db_conn
import aiosqlite

router = APIRouter()

###########################
# third part [homework 4]

class Track(BaseModel):
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: float

@router.get("/tracks")
async def tracks(connection: aiosqlite.Connection = Depends(get_db_conn), page: int = 0, per_page: int = 10):
    cursor = await connection.execute("SELECT * FROM tracks ORDER BY trackid LIMIT ? OFFSET ?;", (per_page, page * per_page))
    data = await cursor.fetchall()
    return data

@router.get("/customers")
async def customers(db_connection: aiosqlite.Connection = Depends(get_db_conn)):
    db_connection.row_factory = aiosqlite.Row
    cursor = await db_connection.execute("SELECT Email FROM customers")
    data = await cursor.fetchall()
    return data