from .. import models, pydantic_model, helpers, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database_handler import engine, get_db
from typing import List, Optional
from sqlalchemy import func

# Note: if I want to the user to be loged in when doing something I can
# just add a dependency in that request

router = APIRouter(
    prefix = "/posts",  # So I don't need to keep adding the same route
    tags = ['Posts']  # To fix the documentation
)


# To retrive data use post request
@router.get("/", response_model = List[pydantic_model.PostLove])
def get_posts(db: Session = Depends(get_db), limit: int = 3, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Basicaly I'm creating a query that will get the amount of loves in a post
    # By doing an count of loves based of an left outer join
    # To check the query just print it
    # For more information on how to do this query check
    # https://helperbyte.com/questions/168146/sql-query-for-fetching-the-post-and-number-of-likes
    # So, to achieve this I had to create an query that does what I want and them figure out a way to do this query
    # using sqlalchemy
    posts_loves = db.query(models.Post, func.count(models.Love.post_id).label("loves")).join(models.Love, models.Love.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return posts_loves


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

    # **post.dict() does the same as title=post.title, ... because it unpacks the dict and puts it in the same format as
    # what was before (title-post.title, content=post.content, ...)
    # OBVIOUS NOTE: This fk_user_id = current_user.id
    # is automatically saying to my db how is creating this post
    new_post = models.Post(fk_user_id = current_user.id, **post.dict())
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

    # Check if this posts belongs to the user that is trying to delete
    if post.fk_user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User not authorized to perform this request")

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

    # Check if this posts belongs to the user that is trying to update
    if post.fk_user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User not authorized to perform this request")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

