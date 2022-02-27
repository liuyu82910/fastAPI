from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote'])

@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), auth_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == auth_user.id).order_by(desc(models.Vote.created_dt))
    result = vote_query.first()
    if result:
        if vote.dir == result.dir:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {auth_user.id} already voted {vote.dir} for post {vote.post_id}")
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = auth_user.id, dir = vote.dir)
            db.add(new_vote)
            db.commit()
            return {"message": f"User {auth_user.id} changes vote from {result.dir} to {vote.dir} for post {vote.post_id}"}
    else:
        new_vote = models.Vote(post_id = vote.post_id, user_id = auth_user.id, dir = vote.dir)
        db.add(new_vote)
        db.commit()
        return {"message": f"User {auth_user.id} votes {vote.dir} for post {vote.post_id}"}