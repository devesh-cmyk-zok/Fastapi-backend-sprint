from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import get_db
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/login",  # all the routes in this router will have the prefix /login, so we don't have to write it in every route
    tags=["Authentication"]  # this will be used to group the routes in the documentation, so that all the routes related to authentication will be grouped together in the documentation
)

''' @router.post("/login")  
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):  # user_credentials is a user object and it will be passed in the request body, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()  # query the database to get the user with the given email, it will return a user object or None if the user is not found # first() will return the first user object that matches the filter condition or None if no user is found

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")  # if the user is not found, raise an HTTPException with a 403 error and a message

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")  # if the password is incorrect, raise an HTTPException with a 403 error and a message

    # Create a token
    token = utils.create_access_token(data={"user_id": user.id})
    return{"access_token": token, "token_type": "bearer"}  # return the generated token '''

# Using OAuth2PasswordRequestForm to handle login form data
@router.post("/login", response_model=schemas.Token)  # response_model is used to specify the type of the response, it can be changed to any other type like dict, list, str etc. depending on the requirement
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  # user_credentials is a user object and it will be passed in the request body, db is a session object and it will be passed to the function as a parameter, we can use it to interact with the database
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  # query the database to get the user with the given email, it will return a user object or None if the user is not found # first() will return the first user object that matches the filter condition or None if no user is found

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")  # if the user is not found, raise an HTTPException with a 403 error and a message

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")  # if the password is incorrect, raise an HTTPException with a 403 error and a message

    # Create a token
    token = utils.create_access_token(data={"user_id": user.id})
    return{"access_token": token, "token_type": "bearer"}  # return the generated token


