from jose import JWTError, jwt
from .config import settings
from datetime import datetime, timedelta
from . import pydantic_model, database_handler, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# How this file works it creates the token, then to verify it the requests will have a dependency which comes from
# get_current_token, which returns if this token is ok or not by returning the result from the verify_access_token
# function

# For more information on how all of this works go to: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# For JWT to work we need:
# SECRET_KEY
# Algorithm
# Expiration time

# This is going be the end point of my login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data: dict):

    # The data that I want to encode as a copy since I don't want to change the data
    to_encode = data.copy()

    # My expiration time starts
    expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Create the token
    jwt_encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_encoded


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = settings.JWT_ALGORITHM)
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = pydantic_model.TokenData(id = user_id)

    except JWTError:
        raise credentials_exception

    return token_data

# Before each path operation was fetching the user from the database, now this function does this automatically
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database_handler.get_db)):

    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
