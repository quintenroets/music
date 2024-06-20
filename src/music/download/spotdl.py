from ..clients import spotdl
from ..context import context

print("import")
downloader = spotdl.Client.create(context.secrets).downloader

print("object")
