
#Python

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Schemas
from api.v1.users.schemas.user import UserOut

# Mixins
from api.v1.mixins.schemas import IDMixin, TimestampMixin

class BaseTweet(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example="The First Tweet"
    )
    
    
class TweetUserID(BaseModel):
    user_id: int = Field(
        ...,
        ge=1,
        title="User ID",
        description="User who created the tweet.",
        example=1
    )
  
    
class CreateTweet(BaseTweet, TweetUserID):
    pass


class TweetOut( TimestampMixin, TweetUserID, BaseTweet, IDMixin):
    class Config:
        orm_mode = True

class TweetWithRelations( TimestampMixin, BaseTweet, IDMixin):

    user: UserOut = Field(...,
                       title='User who created the tweet',)
    
    class Config:
        orm_mode = True

