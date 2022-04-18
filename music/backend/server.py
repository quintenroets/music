from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

import tbhandler

from .artistmanager import ArtistManager

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


@app.exception_handler(Exception)
async def handler(_: Request, exc: Exception):
    tbhandler.show(exit_after=False, repeat=False)
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/newartist")
async def get(name):
    return ArtistManager.search_artists(name)


@app.get("/newsong")
async def get(name):
    return ArtistManager.search_song(name)


@app.get("/addartist")
async def get(id, name):
    return ArtistManager.add_artist(id, name)


@app.get("/addsong")
async def get(id):
    return ArtistManager.add_song(id)


@app.get("/changeartist")
async def get(id):
    return ArtistManager.change_artist(id)


@app.get("/recommendedartists")
async def get():
    return ArtistManager.recommendations()


@app.get("/recommendedsongs")
async def get():
    return ArtistManager.song_recommendations()


@app.get("/artists")
async def get():
    return ArtistManager.artists()
