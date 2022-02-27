from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import and_, case, func

router = APIRouter(
    prefix="/posts",
    tags=['posts'])

@router.get("", response_model=List[schemas.PostResponse])
def get_all_posts_with_kw(db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user), 
limit: int = 100, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post).filter(models.Post.title.ilike(f'%{search}%')).limit(limit).offset(skip).all()
    if not posts:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with search keyword {search} in title was not found!")
    return posts


@router.get("/getall", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    result = db.query(models.Post, func.count(case((models.Like.dir==1, 1))).label('Heart'), func.count(case((models.Like.dir==0, 1))).label('Yuck')).join(models.User, models.Post.user_id==models.User.id, isouter=True).join(models.Like, models.Post.id==models.Like.post_id, isouter=True).group_by(models.Post.id, models.User.id).order_by(models.Post.id).all()
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post")
    return result

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_a_post(post: schemas.Post, db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    # print(auth_user.id)
    new_post = models.Post(user_id=auth_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_a_post(id: int, db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post, func.count(case((models.Like.dir==1, 1))).label('Heart'), func.count(case((models.Like.dir==0, 1))).label('Yuck')).join(models.User, models.Post.user_id==models.User.id, isouter=True).join(models.Like, models.Post.id==models.Like.post_id, isouter=True).group_by(models.Post.id, models.User.id).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    if post.Post.user_id != auth_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"post with id {id} is not authorized to access") 
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int, db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    if post.user_id != auth_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"post with id {id} is not authorized to delete by user {auth_user.email}") 
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(f'post {id} deleted', status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_a_post(id: int, po: schemas.Post, db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    if post.user_id != auth_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"post with id {id} is not authorized to update by user {auth_user.email}") 
    post_query.update(po.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
