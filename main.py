from fastapi import FastAPI

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
