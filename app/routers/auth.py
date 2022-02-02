from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database_handler, pydantic_model, helpers, models, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ['Authentication'])

@router.post('/login', response_model = pydantic_model.AccessToken)
# This function will have 2 dependencies first one will be to retrive the crendentials which will be stored
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database_handler.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # If user not found:
    if user == None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    if not helpers.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Crendentials")

    # Create the token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # return it
    return {'access_token': access_token, "token_type": "bearer"}
