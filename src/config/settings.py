from dotenv import load_dotenv
from pydantic import BaseSettings
import os

# take environment variables from .env.
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Twitter API"
    version: str = "0.0.1"
    admin: str = "Bento Benack"
    


settings = Settings()


# Variables
DEBUG = os.environ.get("DEBUG")
SECRET_KEY = os.environ.get('SECRET_KEY')
PORT = os.environ.get('PORT')

# Database
DATABASE_URL = os.environ.get('DATABASE_URL')

# JWT
ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_TYPE = 'access'
JWT_ACCESS_TOKEN_EXPIRATION = 60 * 24 # 1 day

JWT_REFRESH_TOKEN_TYPE = 'refresh'
JWT_REFRESH_TOKEN_EXPIRATION = 60 * 24 * 7 # 1 week