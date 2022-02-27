from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/like",
    tags=['Like'])

@router.post("", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(get_db), auth_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {like.post_id} does not exist")
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == auth_user.id, models.Like.dir == like.dir)
    like_result = like_query.first()
    delete_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == auth_user.id)
    delete_result = delete_query.first()
    if like.dir == 1:
        if like_result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {auth_user.id} already liked the post {like.post_id}")
        delete_query.delete(synchronize_session=False)
        new = models.Like(post_id=like.post_id, user_id=auth_user.id, dir=like.dir)
        db.add(new)
        db.commit()
        return {"message": f"user {auth_user.id} likes the post {like.post_id}"}
    elif like.dir == 0:
        if like_result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {auth_user.id} already unliked the post {like.post_id}")
        delete_query.delete(synchronize_session=False)
        new = models.Like(post_id=like.post_id, user_id=auth_user.id, dir=like.dir)
        db.add(new)
        db.commit()
        return {"message": f"user {auth_user.id} unlikes the post {like.post_id}"}
    else:
        if not delete_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"user {auth_user.id} never likes or dislikes for post {like.post_id}")
        delete_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"user {auth_user.id} deleted like or dislike post {like.post_id}"}

