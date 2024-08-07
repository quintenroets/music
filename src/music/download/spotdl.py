from music.clients import spotdl
from music.context import context

downloader = spotdl.Client.create(context.secrets).downloader
