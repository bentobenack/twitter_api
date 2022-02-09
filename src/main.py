
from fastapi import FastAPI

from api.v1.users.routes.user import user
from api.v1.tweets.routes.tweet import tweet

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
app.include_router(tweet)