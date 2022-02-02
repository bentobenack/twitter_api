from unicodedata import name
from fastapi import FastAPI

app = FastAPI(
    title="Twitter API",
    description="This is a copy of Twitter API",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Users Routes",
        },
        {
            "name": "Tweets",
            "description": "Tweets Routes",
        }
    ]
)

