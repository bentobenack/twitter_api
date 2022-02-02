
#Python
from datetime import datetime
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Schemas
from schemas.user import UserOut

# Mixins
from core.schemas.mixins.schemas import IDMixin, TimestampMixin

class BaseTweet(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example="The First Tweet"
    )
    
    
class TweetUserID(BaseModel):
    created_by: int = Field(
        ...,
        ge=1,
        title="User ID",
        description="User who created the tweet.",
        example=1
    )
    
    
class Tweet(IDMixin, BaseTweet, TweetUserID, TimestampMixin):
    pass


class CreateTweet(BaseTweet, TweetUserID):
    pass