from fastapi import FastAPI, Response, status, HTTPException
from post_format import Post
from random import randrange

# from fastapi.params import Body

# Note: in FastAPI the order matter. So, if you don't name your path it will take the first one that matches the request
# being made

# VARIABLES:
# Creating an instance of fastapi
app = FastAPI()
post_list =[{"title": "title of post 1", "content": "content of post 1", "id": 1}]

# SEPARATED FUNCTIONS:
# Basic search
def post_search(id):
    for p in post_list:
        if p["id"] == id:
             return p

# Search for array index by Id
def index_serch(id):
    for index, post in enumerate(post_list):
        if post['id'] == id:
            return index


# ROUTES:
# FastAPI changes this masssage to JSON
@app.get("/")
def root():

    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}


# To retrive data use post request
@app.get("/posts")
def get_posts():

    return {"data": post_list} # JSON Format


#Let's create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Body extracts all of the filds from the body, after it converts it to a python dict, and saves it into this
# class called Post that comes from the file post.py(which was a variable before, called body_data)
def create_posts(post: Post):

    # print(post) # Check the terminal for this print
    # print (post.dict()) # Transforming my pydantic model into a dict
    post_dict = post.dict()

    # Make this new id key have random value
    post_dict['id'] = randrange(0, 100000000)
    post_list.append(post_dict)

    return{"data": post_dict}


# Retriving one individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response): # FastAPI is validating the id for me ;)

    # print(int(id))

    post = post_search(int(id))

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
    # Find the index of this id in my array to pop it out
    index = index_serch(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    post_list.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Request
@app.put("/posts/{id}")
def update_post(id: int, post: Post, response: Response):

    # Search for the post's id that I want to change
    index = index_serch(id)

    # Check if it exists
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    # If it exists create the update for the post
    post_dict = post.dict()
    # Make this new creation have the id that I want to change
    post_dict['id'] = id
    # Change the serach found post for this "new post" that I created to replace this old one
    post_list[index] = post_dict

    return {"data": post_dict}
