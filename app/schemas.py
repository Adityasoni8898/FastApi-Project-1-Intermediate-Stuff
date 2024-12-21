import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published:Optional[bool] = True

class CreatePost(PostBase):
    pass

class UserBase(BaseModel):
    email: EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime.datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    owner : UserResponse
    id : int
    created_at : datetime.datetime

    class Config:
        from_attributes = True  # tells the Pydantic to read the given if the given data is not dict, any ORM model works

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0, le=1) # type: ignore