from dataclasses import dataclass

from .path import Path


@dataclass
class Config:
    secrets_path = Path.secrets
    number_of_recommendations: int = 50
    max_new_recommendation_tries: int = 10
    download_chunk_size: int = 20
    download_retries: int = 5
    phone_upload_port: int = 2222
