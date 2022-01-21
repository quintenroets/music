import tbhandler

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from music.data import Data

from ..spotapi import SpotApi
from ..artistmanager import ArtistManager
from ..datamanager import DataManager

app = FastAPI()

origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(Exception)
async def handler(request: Request, exc: Exception):
    tbhandler.show(exit=False)
    return PlainTextResponse(str(exc), status_code=400)


@app.get('/newartist')
async def get(name):
    return DataManager.get_new_artists(name)

@app.get('/addartist')
async def get(id, name):
    return ArtistManager.save('normal', id, name)


@app.get('/changeartist')
async def get(id):
    return DataManager.change_type(id)


@app.get('/recommendedartists')
async def get():
    return ArtistManager.get_recommended_artists()


@app.get('/artists')
async def get():
    artists = Data.artists()
    artists_info = SpotApi.get_artist_infos(artists)
    for a, info in zip(artists, artists_info):
        info['type'] = a.type

    favorites = [a for a in artists_info if a['type'] == 'favorite']
    normal = [a for a in artists_info if a['type'] != 'favorite']
    return favorites + normal
