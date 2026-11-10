from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, utils
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",  # all the routes in this router will have the prefix /vote, so we don't have to write it in every route    
    tags = ["Vote"]  # this will be used to group the routes in the documentation, so that all the routes related to vote will be grouped together in the documentation         
)

@router.post("/", status_code=status.HTTP_201_CREATED)  # status_code is used to set the status code of the response, it can be changed to any other status code like 200, 400, 404 etc. depending on the requirement
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()  # query the database to get the post with the given post_id, it will return a post object or None if the post is not found
    if not post:  # if the post is not found, it means the user is trying to vote on a post that does not exist, so we will raise an exception  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")  # raise an HTTPException with a 404 error and a message   
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)  # query the database to get the vote with the given post_id and user_id, it will return a vote object or None if the vote is not found

    found_vote = vote_query.first()  # get the first vote object that matches the filter condition or None if no vote is found  

    if (vote.dir == 1):  # if the direction of the vote is 1, it means the user wants to upvote the post
        if found_vote:  # if the vote is found, it means the user has already upvoted the post, so we will raise an exception
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")  # raise an HTTPException with a 409 error and a message

        new_vote = models.vote(post_id=vote.post_id, user_id=current_user.id)  # create a new vote object with the given post_id and user_id
        db.add(new_vote)  # add the new vote object to the session
        db.commit()  # commit the session to the database, it will save the new vote
        return {"message": "Successfully added vote"}  # return a message indicating that the vote was successfully added

    else:  # if the direction of the vote is 0, it means the user wants to remove the vote
        if not found_vote:  # if the vote is not found, it means the user has not upvoted the post, so we will raise an exception
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")  # raise an HTTPException with a 404 error and a message

        vote_query.delete(synchronize_session=False)  # delete the vote object from the session
        db.commit()  # commit the session to the database, it will delete the vote
        return {"message": "Successfully deleted vote"}  # return a message indicating that the vote was successfully deleted