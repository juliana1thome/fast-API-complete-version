from .. import models, pydantic_model, helpers, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database_handler import engine, get_db
from typing import List

# Note: if I want to the user to be loged in when doing something I can
# just add a dependency in that request

router = APIRouter(
    prefix = "/posts",  # So I don't need to keep adding the same route
    tags = ['Posts']  # To fix the documentation
)


# To retrive data use post request
@router.get("/", response_model = List[pydantic_model.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


# Retriving one individual post
@router.get("/{id}", response_model = pydantic_model.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):  # FastAPI is validating the id for me ;)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Throw a 404 error and change the error code
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")

    return post


# Let's create posts
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = pydantic_model.PostResponse)
def create_posts(post: pydantic_model.PostCreate, db: Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):

    print(current_user.id)
    # **post.dict() does the same as title=post.title, ... because it unpacks the dict and puts it in the same format as
    # what was before (title-post.title, content=post.content, ...)
    new_post = models.Post(**post.dict())
    # Add in the db
    db.add(new_post)
    # Commit your changes in the db
    db.commit()
    # Retrive this this new post and store it back in the variable called new_post
    db.refresh(new_post)

    return new_post


# Delete Request
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Request
@router.put("/{id}", response_model = pydantic_model.PostResponse)
def update_post(id: int, updated_post: pydantic_model.PostCreate, response: Response, db: Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check if it exists
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

