from dataclasses import dataclass

from .path import Path


@dataclass
class Config:
    secrets_path = Path.secrets
    download_chunk_size: int = 20
    download_retries: int = 5
    phone_upload_port: int = 2222
    frontend_port: int = 8080
