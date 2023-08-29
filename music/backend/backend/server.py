import tbhandler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from . import artistmanager

app = FastAPI()

origins = [f"http://localhost:{8080}"]
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
    return artistmanager.search_artists(name)


@app.get("/newsong")
async def get(name):
    return artistmanager.search_song(name)


@app.get("/addartist")
async def get(id, name):
    return artistmanager.add_artist(id, name)


@app.get("/addsong")
async def get(id):
    return artistmanager.add_song(id)


@app.get("/changeartist")
async def get(id):
    return artistmanager.change_artist(id)


@app.get("/recommendedartists")
async def get():
    return artistmanager.recommendations()


@app.get("/recommendedsongs")
async def get():
    return artistmanager.song_recommendations()


@app.get("/artists")
async def get():
    return artistmanager.artists()
