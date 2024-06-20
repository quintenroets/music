from ..clients import spotdl
from ..context import context

downloader = spotdl.Client.create(context.secrets).downloader
