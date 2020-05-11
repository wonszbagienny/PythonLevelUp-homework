from fastapi import APIRouter, Response, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict
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
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute("SELECT Name FROM tracks WHERE Composer = ? ORDER BY Name;", (composer_name, ))
    data = await cursor.fetchall()
    if not data:
        raise HTTPException(status_code=404, detail={"error": "composer not found"})
    return data

class Album(BaseModel):
    title: str
    artist_id: int

class AlbumResponse(BaseModel):
    AlbumId: int
    title: str
    artist_id: int

@router.post("/albums", status_code=201, response_model=AlbumResponse)
async def post_album(request: Album):
    cursor = await router.db_connection.execute("SELECT ArtistId FROM artists WHERE ArtistId = ?;", (request.artist_id,))
    check = await cursor.fetchone()
    if not check:
        raise HTTPException(status_code=404, detail={"error": "artist_id not found"})
    cursor = await router.db_connection.execute("INSERT INTO albums (Title, ArtistId) VALUES (?, ?);", (request.title, request.artist_id))
    await router.db_connection.commit()
    return AlbumResponse(AlbumId = cursor.lastrowid, title = request.title, artist_id = request.artist_id)
    #return {"AlbumId": cursor.lastrowid, "Title": request.title, "ArtistId": request.artist_id}

@router.get("/albums/{album_id}", status_code=200)
async def get_album(album_id: int):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute("SELECT * FROM albums WHERE AlbumId = ?;", (album_id,))
    album = await cursor.fetchone()
    if not album:
        raise HTTPException(status_code=404, detail={"error": "artist_id not found"})
    return album