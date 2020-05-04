from fastapi import APIRouter, Response, status
from pydantic import BaseModel
import aiosqlite

router = APIRouter()

###########################
# third part [homework 4]

@app.on_event("startup")
async def startup():
    router.db_connection = await aiosqlite.connect('databases/chinook.db')

@app.on_event("shutdown")
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

@router.get("/tracks", response_model=List[Track])
async def tracks(connection: aiosqlite.Connection = Depends(get_db_conn), page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.dob_connection.execute("SELECT * FROM tracks ORDER BY trackid LIMIT ? OFFSET ?;", (per_page, page * per_page))
    data = await cursor.fetchall()
    return data

@router.get("/customers")
async def customers(db_connection: aiosqlite.Connection = Depends(get_db_conn)):
    db_connection.row_factory = aiosqlite.Row
    cursor = await db_connection.execute("SELECT Email FROM customers")
    data = await cursor.fetchall()
    return data