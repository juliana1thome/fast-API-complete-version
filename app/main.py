from fastapi import FastAPI
from . import models
from .database_handler import engine
from .routers import post, user, auth

# Create all my models
models.Base.metadata.create_all(bind=engine)

# Creating an instance of fastapi
app = FastAPI()

# So, the main idea is that I used a route object to separate my path operation in different files
# And I imported them by doing this thing down here ;)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# FastAPI changes this masssage to JSON
@app.get("/")
def root():

    return{"message": "ʕ•́ᴥ•̀ʔっWelcome to Juliana's API"}
