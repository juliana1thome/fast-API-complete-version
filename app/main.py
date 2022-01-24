from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
from .database_connect import connect
from . import models, pydantic_model, helpers
from .database_handler import engine, get_db
from sqlalchemy.orm import Session
from typing import List

# Create all my models
models.Base.metadata.create_all(bind=engine)

# VARIABLES:
# Creating an instance of fastapi
app = FastAPI()
post_list = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]

# ROUTES:
# FastAPI changes this masssage to JSON
@app.get("/")
def root():

    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}


# To retrive data use post request
@app.get("/posts", response_model=List[pydantic_model.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    # If you print this without this all method, you will see that this is just a sql command
    posts = db.query(models.Post).all()

    # How to do it in raw SQL:
    # connect.cursor.execute("""SELECT * FROM posts""")
    # posts = connect.cursor.fetchall()

    return posts


# Retriving one individual post
@app.get("/posts/{id}", response_model=pydantic_model.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):  # FastAPI is validating the id for me ;)

    # .filter = WHERE in sql
    # So... we use .all to get all the things you are looking for
    # But, here we would "waste time and resources" at making our app look for all of them
    # So, to fix this we use the first that is the one we are looking for
    # EFFICIENCY! ヽ(°〇°)ﾉ
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # How to do it in raw SQL:
    # connect.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = connect.cursor.fetchone()

    # Throw a 404 error and change the error code
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")

        # Hard code the Raise exception ↓
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}

    return post


# Let's create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=pydantic_model.PostResponse)
def create_posts(post: pydantic_model.PostCreate, db: Session = Depends(get_db)):

    # **post.dict() does the same as title=post.title, ... because it unpacks the dict and puts it in the same format as
    # what was before (title-post.title, content=post.content, ...)
    new_post = models.Post(**post.dict())
    # Add in the db
    db.add(new_post)
    # Commit your changes in the db
    db.commit()
    # Retrive this this new post and store it back in the variable called new_post
    db.refresh(new_post)

    # How to do it in raw SQL:
    # WHY NOT: cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title}, {post.content},
    # {post.published})") ?
    # Because it is vunerable to SQL injection. For example, if in the title the user decide to pass a sql statement you
    # will be vunerable to that ;)
    # So to sanitize the input use the %s
    # connect.cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""", (post.title, post.content, post.published))
    # To return the value added just fetch it and return it later
    # new_post = connect.cursor.fetchone
    #connect.conn.commit()

    return new_post


# Delete Request
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # How to do it in raw SQL:
    # connect.cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = connect.cursor.fetchone()
    # connect.conn.commit()

    # If it does not exist return an "error", but pay attention to the first() method if you are
    # curious to understand what is this go to get method by id
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    # But if it exists delete it
    # SQLAlchemy: synchronize_session – chooses the strategy to update the attributes on objects in the session.
    # Note: SQLAlchemy is a orm ;)
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Request
@app.put("/posts/{id}", response_model=pydantic_model.PostResponse)
def update_post(id: int, updated_post: pydantic_model.PostCreate, response: Response, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # How to do it in raw SQL:
    # connect.cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = connect.cursor.fetchone()
    # connect.conn.commit()

    # Check if it exists
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    # updated_post.dict() is the same as {'title': 'title added by user', 'content': 'content added by user'}
    # Since it get the user input and transforms it into a dict
    # Silly Note: updated_post comes from the pydantic model so the user enters an input that follows the model
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# Handling requests for users table

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = pydantic_model.UserResponse)
def create_user(user: pydantic_model.UserCreate, db: Session = Depends(get_db)):
    # Before creating the user you will need to hash the password
    hashed_passw = helpers.hash(user.password)
    # Now make it real :P
    user.password = hashed_passw

    new_user = models.User(**user.dict())  # Convert it to a dict and unpack it
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
