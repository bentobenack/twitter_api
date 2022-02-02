
from fastapi import FastAPI

from v1.routes.user import user

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

app.include_router(user)