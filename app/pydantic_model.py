from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Defining my schema
# This makes you have a easier time extracting the data. So, you can only do this to extract title
# new_post.title (check main.py file to understand where this new_post comes from)
# Also, it performs an validation

########################
### Schema for Posts ###
########################

# This is my Pydantic model and it is for shape our request
# Shape of our Request
class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True # Default True


class PostCreate(PostBase):
    pass


# Shape of our Response (that is us passing data to the user)
class PostResponse(PostBase):

    id: int
    created_at: datetime

    # The pydantic model will only read if it is a dict
    # So, we need something to convert the SQLAlchemy model to Pydantic model
    class Config:
        orm_mode = True

########################
### Schema for Users ###
########################
class UserCreate(BaseModel):
    # For this to work you need to have email-validator installed
    # To check if you have it does type pip freeze on your terminal
    # Also this EmailStr does the email validation for me
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
