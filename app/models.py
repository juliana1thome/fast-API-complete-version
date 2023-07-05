from .database_handler import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# SQL Alchemy model
# Define how all tables will look like
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default = 'True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    fk_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # It will create another property for Post class
    # That will return the relationship between Post class and User class
    # That means this will fetch the user's id for me and return it
    owner = relationship("User")

# To handle registration create a table that will save our users info
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# In order to handle votes/likes I need a table that will save this info
# And a relation between likes, posts and users is a must
# This table will be call Love instead of vote or like just for the fun ¯\_( ͡❛ ͜ʖ ͡❛)_/¯_
class Love(Base):
    __tablename__ = "loves"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
