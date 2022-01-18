from pydantic import BaseModel
from typing import Optional

# Defining my schema
# This makes you have a easier time extracting the data. So, you can only do this to extract title
# new_post.title (check main.py file to understand where this new_post comes from)
# Also, it performs an validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Default True
    rating: Optional[int] = None # Fully optional
