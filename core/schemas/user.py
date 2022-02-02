
#Python
from datetime import date
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel, validator
from pydantic import EmailStr
from pydantic import Field

class UserBase(BaseModel):
    user_id: Optional[UUID]= Field(default=None)
    email: EmailStr = Field(..., example="benackk@email.com")


class UserPassword(BaseModel):
     password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="H4rdP455w0rd"
    )
     
     
class UserLogin(UserBase, UserPassword):
    pass    


class User(UserBase):
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
    birth_date: Optional[date] = Field(default=None, example="2022-02-01")
    
    #Validate the age. Must be over 18
    @validator('birth_date')
    def is_over_eighteen(cls, v):
        todays_date = date.today()
        delta = todays_date - v

        if delta.days/365 <= 18:
            raise ValueError('Must be over 18!')
        else:
            return v
    
class UserRegister(User, UserPassword):
    pass