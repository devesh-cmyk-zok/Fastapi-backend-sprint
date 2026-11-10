from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func
from app import oauth2
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/posts",  # all the routes in this router will have the prefix /posts, so we don't have to write it in every route
    tags=["Posts"]  # this will be used to group the routes in the documentation, so that all the routes related to posts will be grouped together in the documentation
)
    
# GET POSTS
# @router.get("/", response_model= List[schemas.Post])  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
@router.get("/", response_model= List[schemas.PostOut])  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
def get_posts(db: Session = Depends(get_db), current_user : int  = Depends(oauth2.get_current_user),
              limit : int = 10, skip: int = 0, search : Optional[str] = "beach"):  # db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database
    
  # post = db.query(models.Post).limit(limit).offset(skip).filter(models.Post.tile.contains(search)).all()  # query the database to get all the posts, it will return a list of post objects

    # search is used to search keywords in the title of the posts, it will be passed in the url as a query parameter, if not provided it will default to "beach", url example: http://?search=beach
    # used at &search = keyword1%20keyword2%20keyword3, %20 is used to represent a space in the url, so the above url will search for posts that contain "keyword1 keyword2 keyword3" in the title

    # skip is used as a query parameter to skip the first n posts, it will be passed in the url as a query parameter, if not provided it will default to 0, url example: http://?skip=5
    # &skip=2
    
    # JOINS USING SQLALCHEMY
    post = db.query(models.Post, func.count(models.Vote.Post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
     # query the database to get all the posts, it will return a list of post objects

    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{id} not found")
    
    if post.owner_id != current_user.id:  # check if the owner_id of the post is equal to the id of the current user, if not raise an exception
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action") 

    print(limit) # print the limit value for debugging purposes  # limit is used as a query parameter to limit the number of posts returned, it will be passed in the url as a query parameter, if not provided it will default to 10, url example: http://?limit=5

    return post  # return the list of post objects as a dictionary with the id added

# CREATE POSTS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  # status_code is used
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):  # db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database

    # create a new post object using the post class and the data from the request body
 #  new_post = models.Post(
 #      title=post.title, content=post.content, published=post.published)  
    
    # Alternate better way
    print(**post.dict())  # convert the post object to a dictionary

    new_post = models.Post(owner_id=current_user.id, **post.dict())  # Automatically unpack the dictionary and pass the values to the Post class constructor
    
    print(current_user.id)  # get the user id from the token data and print it for debugging purposes
    print(current_user.email)  # get the user id from the token data and print it for debugging purposes
    db.add(new_post)  # add the new post object to the session
    db.commit()  # commit the session to the database, it will save the new post
    db.refresh(new_post)  # refresh the new post object to get the id from the database, it will update the new post object with the id from the database

    return {"data" : new_post}  # return the new post object as a dictionary with the id added

# GET POST BY ID
@router.get("/{id}", response_model=schemas.PostOut)  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
def get_post(id: int, db: Session = Depends(get_db), current_user : int  = Depends(oauth2.get_current_user),):
      # id is an integer and it will be passed in the url as a path parameter, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database
    post = db.query(models.Post).filter(models.Post.id == id).first()  # query the database to get the post with the given id, it will return a post object or None if the post is not found # first() will return the first post object that matches the filter condition or None if no post is found

    post = db.query(models.Post, func.count(models.Vote.Post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()  # query the database to get the post with the given id, it will return a post object or None if the post is not found # first() will return the first post object that matches the filter condition or None if no post is found
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")  
        
    return {"post_details": f"Post with id {id} has been retrieved"}  

# DELETE POST BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  # status_code is used to set the status code of the response, it can be changed to any other status code like 200, 400, 404 etc. depending on the requirement
def delete_posts(id:int, db: Session = Depends(get_db), current_user : int  = Depends(oauth2.get_current_user)):  # id is an integer and it will be passed in the url as a path parameter, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database

    post_query = db.query(models.Post).filter(models.Post.id == id)  # query the database to get the post with the given id, it will return a post object or None if the post is not found # first() will return the first post object that matches the filter condition or None if no post is found

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{id} not found")

    if post.owner_id != current_user.id:  # check if the owner_id of the post is equal to the id of the current user, if not raise an exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")  # 403 is used to indicate that the user is not authorized to perform the requested action

    post_query.delete(synchronize_session=False)  # delete the post object from the session, synchronize_session=False is used to avoid a warning message
    db.commit()  # commit the session to the database, it will delete the post from the database

# UPDATE POST BY ID
@router.put("/{id}", response_model=schemas.Post)  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int  = Depends(oauth2.get_current_user)):  # id is an integer and it will be passed in the url as a path parameter, post is a post object and it will be passed in the request body, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database
    
    post_query = db.query(models.Post).filter(models.Post.id == id)  # query the database to get the post with the given id, it will return a post object or None if the post is not found # first() will return the first post object that matches the filter condition or None if no post is found
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{id} not found")

    if post.owner_id != current_user.id:  # check if the owner_id of the post is equal to the id of the current user, if not raise an exception
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")  # 403 is used to indicate that the user is not authorized to perform the requested action
    
    post_query.update(updated_post.dict(), synchronize_session=False)  # update the post object in the session, synchronize_session=False is used to avoid a warning message
    db.commit()  # commit the session to the database, it will update the post in the database

    return {"data": post_query.first()}  # return the updated post object as a dictionary