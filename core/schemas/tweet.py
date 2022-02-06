
#Python

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Schemas
from core.schemas.user import UserOut

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
    pass

class TweetWithRelations( TimestampMixin, BaseTweet, IDMixin):

    user: UserOut = Field(...,
                       title='User who created the tweet',)

