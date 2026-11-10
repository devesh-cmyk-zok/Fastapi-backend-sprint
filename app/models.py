from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import base

class Post(base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)  
    published = Column(Boolean, server_default='TRUE', nullable = False)  # server_default is used to set the default value of the column in the database
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))  # server_default is used to set the default value of the column in the database

    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)  # owner_id is a foreign key that references the id column of the users table, it is used to establish a relationship between the posts and users tables

    owner = relationship("User")  # relationship is used to establish a relationship between the posts and users tables, it is used to access the user object from the post object
    
class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique=True)  # unique is used to set the unique constraint on the column in the database
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))  # server_default is used to set the default value of the column in the database

class vote(base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  # ondelete is used to set the cascade delete constraint on the foreign key in the database, it will delete the vote if the user is deleted
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)  # ondelete is used to set the cascade delete constraint on the foreign key in the database, it will delete the vote if the post is deleted
