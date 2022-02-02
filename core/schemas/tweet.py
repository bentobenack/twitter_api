
#Python
from datetime import datetime
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#App 
from schemas.user import User


class Tweet(BaseModel):
    tweet_id: Optional[UUID] = Field(default=None)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example="The First Tweet"
    )
    created_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    created_by: User = Field(...)
    