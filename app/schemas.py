from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint  # conint is used to define a constrained integer type, it can be used to define a integer type with a minimum and maximum value

# class Post(BaseModel): 
#    title: str
#    content: str
#    published: bool = True  # default value is True, if not provided in the request body, it will be set to True

# class CreatePost(BaseModel):
#   title: str
#    content: str
#    published: bool = True  # default value is True, if not provided in the request body, it will be set to True

#class UpdatePost(BaseModel):
#    title: str
#    content: str
#    published: bool

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(BaseModel):
    pass

class Post(PostBase):   # Extending the PostBase class to include id and created_at fields
    id: int
    created_at: datetime
    owner_id: int
    owner : "UserOut"  # This is a forward reference to the UserOut class, which will be defined later

    class config:
        orm_mode = True  # this will tell pydantic to read the data even if it is not a dict, but an ORM model (like SQLAlchemy model)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

#  Doesnt include password in the response model for security reasons
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] | None = None  # id can be None if the token is invalid or expired

class Vote(BaseModel):
    post_id: int
    dir: conint  # direction of the vote, 1 for upvote, 0 for downvote

class PostOut(PostBase):
    post : Post
    votes : int 

    class Config:
        orm_mode = True