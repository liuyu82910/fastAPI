from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import and_, case, func
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=['Users'])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_a_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    post = db.query(models.User).filter(models.User.email==user.email).all()
    if post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Duplicate user with {user.email}")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/all", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), auth_user: str = Depends(oauth2.get_current_user)):
    users = db.query(models.User, func.count(case((models.Like.dir==1, 1))).label('Heart'), func.count(case((models.Like.dir==0, 1))).label('Yuck')).join(models.Like, models.User.id == models.Like.user_id, isouter=True).group_by(models.User.id).order_by(models.User.id.desc()).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No users can be found!")
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def get_a_user(id: int, db: Session = Depends(get_db),  auth_user: str = Depends(oauth2.get_current_user)):
    user = db.query(models.User, func.count(case((models.Like.dir==1, 1))).label('Heart'), func.count(case((models.Like.dir==0, 1))).label('Yuck')).join(models.Like, models.User.id == models.Like.user_id, isouter=True).group_by(models.User.id).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found!")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(id: int, db: Session = Depends(get_db),  auth_user: str = Depends(oauth2.get_current_user)):
    if auth_user.id != 24:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Your user id {auth_user.id} is not authorized to delete a user")
    elif auth_user.id == 24 and id == 24:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You logged in as superuser {auth_user.id}, cannot delete yourself")
    delete_query = db.query(models.User).filter(models.User.id == id)
    result = delete_query.first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} cannot be found, please provide another user id")
    delete_query.delete(synchronize_session=False)
    db.commit()
    return {"Message": f"User {id} is deleted"}
