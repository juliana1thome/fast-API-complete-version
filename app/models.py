from .database_handler import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# This one is the SQL Alchemy model
# And it defines how our database (the table) will look like
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

# To handle registration we need a table that will save our users info
# So, let's create it
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
