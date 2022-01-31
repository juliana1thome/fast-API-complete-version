from jose import JWTError, jwt
from .config import settings
from datetime import datetime, timedelta

# For JWT to work we need:
# SECRET_KEY
# Algorithm
# Expiration time


def create_access_token(data: dict):

    # The data that I want to encode as a copy since I don't want to change the data
    to_encode = data.copy()

    # My expiration time starts
    expire = datetime.now() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Create the token
    jwt_encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_encoded
