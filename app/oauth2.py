# Create a function to create a JWT token using the jose library, which will be used to authenticate the user and authorize access to the protected routes in the application. The function will take a dictionary of data as input, which will be encoded into the JWT token along with an expiration time. The function will return the encoded JWT token as a string.

from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import models, schemas
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .database import engine, get_db

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # this will be used to get the token from the request header, it will be used in the dependency injection of the protected routes

# SECRET KEY
# ALGORITHM
# ACCESS TOKEN EXPIRE MINUTES

SECRET_KEY = settings.secret_key  # "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = settings.algorithm  # "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # '''30'''  ''' 30 minutes '''

def create_access_token(data: dict):

    to_encode = data.copy()  # create a copy of the data dictionary to avoid modifying the original data

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # calculate the expiration time
    to_encode.update({"exp": expire})  # add the expiration time to the data dictionary

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # encode the data dictionary into a JWT token using the secret key and algorithm

    return encoded_jwt  # return the encoded JWT token

def verify_access_token(token: str, credentials_exception):
    """
    Verifies the validity of a JWT token.

    Args:
        token (str): The JWT token to be verified.
        credentials_exception: The exception to be raised if the token is invalid.

    Returns:
        dict: The decoded payload of the JWT token if valid.

    Raises:
        credentials_exception: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # decode the JWT token using the secret key and algorithm
        id: str = payload.get("user_id")  # extract the user_id from the decoded payload

        if id is None:
            raise credentials_exception  # if user_id is not found in the payload, raise an exception
        token_data = schemas.TokenData(id=id)  # create a TokenData object with the extracted user_id

    except JWTError as e:
        print(f"JWTError: {e}")  # print the error message for debugging purposes
        print(f"Token: {token}")  # print the token for debugging purposes

        raise credentials_exception  # if there is an error decoding the token, raise an exception
    return token_data  # return the TokenData object containing the user_id

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        token (str): The JWT token extracted from the request header.

    Returns:
        dict: The decoded payload of the JWT token if valid.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)  # verify the token and get the decoded payload
    user = db.query(models.User).filter(models.User.id == token.id).first()  # query the database to get the user with the given id, it will return a user object or None if the user is not found
    
    return user  # verify the token and return the decoded payload