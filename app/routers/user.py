from .. import models, pydantic_model, helpers
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database_handler import engine, get_db

router = APIRouter(
    prefix = "/users",  # So I don't need to keep adding the same route
    tags = ['Users']  # To fix the documentation
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = pydantic_model.UserResponse)
def create_user(user: pydantic_model.UserCreate, db: Session = Depends(get_db)):
    # Before creating the user you will need to hash the password
    hashed_password = helpers.hash(user.password)
    # Now make it real :P
    user.password = hashed_password

    new_user = models.User(**user.dict())  # Convert it to a dict and unpack it
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model = pydantic_model.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    # If not found:
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exit")

    return user
