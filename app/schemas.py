from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from pydantic.types import conint

class Post(BaseModel):
    title: str
    content: str
    # category: str
    published: bool = True

class Product(BaseModel):
    # id: int
    name: str
    price: float
    # is_sale: bool = False
    inventory: int = 20
    # created_dt: datetime
    # rating: Optional[int] = None

class Productpatch(BaseModel):
     name: Optional[str]
     price: Optional[float]
     inventory: Optional[int] = 30

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: Optional[str]

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_dt: date

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    User: UserResponse
    Heart: int
    Yuck: int
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_dt: datetime
    user_id: int
    user_info: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    Heart: int
    Yuck: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: EmailStr
    epoch_time: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=-1) = 0

class Like(BaseModel):
    post_id: int
    # dir: Optional[conint](le=1, ge=0)
    dir: conint(le=1, ge=-1)