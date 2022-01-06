from fastapi import FastAPI, Form, Response, Header, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
import os

from libs import env
from music.path import Path

env.load(path=Path.env)  # load env here before it is used in other files

from libs.errorhandler import ErrorHandler

from ..spotapi import SpotApi
from ..artistmanager import ArtistManager
from ..datamanager import DataManager

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def handler(request: Request, exc: Exception):
    #ErrorHandler.show_error()
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/newartist")
async def get(name):
    return DataManager.get_new_artists(name)

@app.get("/addartist")
async def get(id, name):
    return ArtistManager.save("normal", id, name)

@app.get("/changeartist")
async def get(id):
    artists = DataManager.get_artists()
    for a in artists:
        if a["id"] == id:
            a["type"] = "favorite" if a["type"] == "normal" else "normal"
            print(a["type"] == "")
            print(a["type"])
            break

    DataManager.save_artists(artists)
    return True

@app.get("/recommendedartists")
async def get():
    return ArtistManager.get_recommended_artists()

@app.get("/artists")
async def get():
    artists = DataManager.get_artists()
    artists_info = SpotApi.get_artist_infos(artists)
    for a, info in zip(artists, artists_info):
        info["type"] = a["type"]

    favorites = [a for a in artists_info if a["type"] == "favorite"]
    normal = [a for a in artists_info if a["type"] != "favorite"]
    return favorites + normal
