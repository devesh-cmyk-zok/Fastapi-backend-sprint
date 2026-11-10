from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, utils

from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/users",  # all the routes in this router will have the prefix /users, so we don't have to write it in every route
    tags=["Users"]  # this will be used to group the routes in the documentation, so that all the routes related to users will be grouped together in the documentation
)

# FOR USERS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # status_code is used to set the status code of the response, it can be changed to any other status code like 200, 400, 404 etc. depending on the requirement
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  # user is a user object and it will be passed in the request body, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database

    # Hash the password before saving it to the database
    hashed_password = utils.hash_password(user.password)  # hash the password using the bcrypt algorithm
    user.password = hashed_password  # update the user object with the hashed password


    # Saving the user to the database
    new_user = models.UserCreate(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user}  # return the user object as a dictionary

# GET USER BY ID
@router.get("/{id}", response_model=schemas.UserOut)  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
def get_user(id: int, db: Session = Depends(get_db)):  # id is an integer and it will be passed in the url as a path parameter, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database

    user = db.query(models.User).filter(models.User.id == id).first()  # query the database to get the user with the given id, it will return a user object or None if the user is not found # first() will return the first user object that matches the filter condition or None if no user is found
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")  # if the user is not found, raise an HTTPException with a 404 error and a message
        
    return {"user_details": f"User with id {id} has been retrieved"}  # return the user object as a dictionary with the id added;