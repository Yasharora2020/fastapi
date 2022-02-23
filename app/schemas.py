from pydantic import BaseModel, BaseSettings, EmailStr
from pydantic.types import OptionalInt, Optional,conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    #id: int
    title: str
    content: str
    published : bool = True   # it creates an optional field with default true
    #created_at: datetime
    

class UserResponse(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime


    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id : int
    owner : UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes:int

    class Config:
        orm_mode = True






class UserCreate(BaseModel):
    email : EmailStr
    password : str

    



class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)




    

