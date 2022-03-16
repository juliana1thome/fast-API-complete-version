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


################################
### Schema for UsersResponse ###
################################

# This pydantic class is here now because since python reads top to bottom
# It would have a problem when PostResponse class calls for it
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


###############################
### Schema for PostResponse ###
###############################

# Shape of our Response (that is us passing data to the user)
class PostResponse(PostBase):

    id: int
    created_at: datetime
    fk_user_id: int
    owner: UserResponse

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

class UserLogin(BaseModel):
    email: EmailStr
    password: str


########################
### Schema for Token ###
########################

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
