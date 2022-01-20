from fastapi import FastAPI, Response, status, HTTPException
from .post_format import Post
from random import randrange
from .database_connect import connect

# from fastapi.params import Body

# Note: in FastAPI the order matter. So, if you don't name your path it will take the first one that matches the request
# being made

# VARIABLES:
# Creating an instance of fastapi
app = FastAPI()
post_list = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]

# SEPARATED FUNCTIONS:

# ROUTES:
# FastAPI changes this masssage to JSON
@app.get("/")
def root():

    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}


# To retrive data use post request
@app.get("/posts")
def get_posts():
    connect.cursor.execute("""SELECT * FROM posts""")
    posts = connect.cursor.fetchall()
    print(posts)
    return {"data": posts}  # JSON Format


# Let's create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    # WHY NOT: cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title}, {post.content},
    # {post.published})") ?
    # Because it is vunerable to SQL injection. For example, if in the title the user decide to pass a sql statement you
    # will be vunerable to that ;)
    # So to sanitize the input use the %s
    connect.cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""", (post.title, post.content, post.published))

    # To return the value added just fetch it and return it later
    new_post = connect.cursor.fetchone

    connect.conn.commit()

    # TODO: figure it out why it works but does not show up the new_post :?
    return{"data": new_post}


# Retriving one individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):  # FastAPI is validating the id for me ;)

    connect.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = connect.cursor.fetchone()

    # Throw a 404 error and change the error code
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")

        # Hard code the Raise exception ↓
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}

    return {"post_detail": post}


# Delete Request
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):

    connect.cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = connect.cursor.fetchone()

    connect.conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Request
@app.put("/posts/{id}")
def update_post(id: int, post: Post, response: Response):

    connect.cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    updated_post = connect.cursor.fetchone()

    connect.conn.commit()

    # Check if it exists
    if updated_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    return {"data": updated_post}
