from fastapi import FastAPI
from post_format import Post
from random import randrange

# from fastapi.params import Body

# Note: in FastAPI the order matter. So, if you don't name your path it will take the first one that matches the request
# being made

# Creating an instance of fastapi
app = FastAPI()

my_posts =[{"title": "title of post 1", "content": "content of post 1", "id": 1}]

# FastAPI changes this masssage to JSON
@app.get("/")

def root():

    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}

# To retrive data use post request
@app.get("/posts")

def get_posts():

    return {"data": my_posts} # JSON Format


#Let's create posts
@app.post("/posts")

# Body extracts all of the filds from the body, after it converts it to a python dict, and saves it into this
# class called Post that comes from the file post.py(which was a variable before, called body_data)

def create_posts(post: Post):

    # print(post) # Check the terminal for this print
    # print (post.dict()) # Transforming my pydantic model into a dict
    post_dict = post.dict()

    # Make this new id key have random value
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)

    return{"data": post_dict}


# Retriving one individual post
@app.get("/posts/{id}")
def get_post(id):
    print(id)

    return {"post_detail": f"This is the post {id}"}
