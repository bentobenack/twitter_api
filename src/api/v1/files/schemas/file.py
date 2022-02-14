
#Python

#Pydantic
from typing import Optional
from pydantic import BaseModel
from pydantic import Field

#Schemas


# Mixins
from api.v1.mixins.schemas import IDMixin, TimestampMixin

class BaseFile(BaseModel):
    file_url: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example="The File URL"
    )
    
    
class FileUserID(BaseModel):
    user_id: Optional[int] = Field(
        default=None,
        ge=1,
        title="User ID",
        description="User who created the file.",
        example=1
    )
    
class FileTweetID(BaseModel):
    tweet_id: Optional[int] = Field(
        default=None,
        ge=1,
        title="Tweet ID",
        description="Tweet ID",
        example=1
    )
  
    
class CreateFile(FileTweetID, FileUserID, BaseFile):
    pass


class FileOut( TimestampMixin, FileTweetID, FileUserID, BaseFile, IDMixin):
    class Config:
        orm_mode = True

