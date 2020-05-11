from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import List
import aiosqlite

router = APIRouter()

###########################
# third part [homework 4]

@router.on_event("startup")
async def startup():
    router.db_connection = await aiosqlite.connect('chinook.db')

@router.on_event("shutdown")
async def shutdown():
    await router.db_connection.close()

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
async def tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT * FROM tracks ORDER BY TrackId LIMIT ? OFFSET ?;", (per_page, page * per_page))
    data = await cursor.fetchall()
    return data

@router.get("/tracks/composers/")
async def composers(composer_name: str):
    db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await db_connection.execute("SELECT Name FROM tracks WHERE Composer = ?", (composer_name))
    data = await cursor.fetchall()
    if len(data) == 0:
        raise HTTPException(status_code=404, detail="error")
    return data