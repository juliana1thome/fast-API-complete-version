from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database_handler, pydantic_model, helpers, models

router = APIRouter(tags = ['Authentication'])


@router.post('/login')
def login(user_crendentials: pydantic_model.UserLogin, db: Session = Depends(database_handler.get_db)):

    user = db.query(models.User).filter(models.User.email == user_crendentials.email).first()

    # If user not found:
    if user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Credentials")

    if not helpers.verify(user_crendentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Crendentials")

    # Add Creation of token
    # return it
    return {'token': 'token'}

