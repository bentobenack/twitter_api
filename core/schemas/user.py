
#Python
from datetime import date
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel, validator
from pydantic import EmailStr
from pydantic import Field

from core.schemas.mixins.schemas import IDMixin, TimestampMixin


class PasswordMixin(BaseModel):
     password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        example="H4rdP455w0rd"
    )
     

class BaseUser(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Bento"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Benack"
    )
    email: EmailStr = Field(..., example="benack@email.com")
    birth_date: Optional[date] = Field(default=None, example="2000-01-01")
    
    #Validate the age. Must be over 18
    @validator('birth_date')
    def is_over_eighteen(cls, v):
        todays_date = date.today()
        delta = todays_date - v

        if delta.days/365 <= 18:
            raise ValueError('Must be over 18!')
        else:
            return v
    
    
    
class UserOut(TimestampMixin, BaseUser, IDMixin):
    pass    


class User(PasswordMixin, UserOut):
    pass
    
    
class CreateUser(PasswordMixin, BaseUser):
    pass