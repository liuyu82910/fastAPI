from unittest.mock import Base
from fastapi import FastAPI, Request, Response, status, HTTPException, Path, Query, Depends
from random import randrange
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from . import models, schemas, utils
from .database import engine, get_db, get_psycopg2
from .routers import post, user, auth, vote, like, product
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(like.router)
app.include_router(product.router)

my_posts = [{"title": "fave book", "user": "Sacha Powell", "content": "silent patient", "category": "reading", "id": 100},
            {"title": "fave food", "user": "Sacha Powell", "content": "mozzarella", "category": "eating", "id": 200}]


def find_post(id):
    return [post for post in my_posts if post['id'] == id]


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


def find_id():
    return [post['id'] for post in my_posts]

@app.get("/")
async def root():
    return {"message": "Hello Sacha Powell"}





