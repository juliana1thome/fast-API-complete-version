from fastapi import FastAPI
from fastapi.params import Body
# Note: in FastAPI the order matter. So, if you don't name your path it will take the first one that matches the request
# being made

# Creating an instance of fastapi
app = FastAPI()

# FastAPI changes this masssage to JSON
@app.get("/")
def root():
    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}

# To retrive data use post request
@app.get("/posts")
def get_posts():
    return {"data": "This is your retrived posts"}


#Let's create posts
@app.post("/create")
# Body extracts all of the filds from the body, after it converts it to a python dict, and saves it into this variable
# called body_data
def create_posts(body_data: dict = Body(...)):
    print(body_data) # Check the terminal for this print
    return{"new_post": f"title: {body_data['title']} content: {body_data['content']}"}


