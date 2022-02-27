from fastapi import Response, status, HTTPException, Depends, APIRouter, Path, Query, Depends
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db, engine, get_psycopg2
from sqlalchemy import and_, case, func

router = APIRouter(
    prefix="/product",
    tags=['products'])
conn = get_psycopg2()
cursor = conn.cursor()


@router.get("")
def get_all_products():
    cursor.execute('''SELECT * 
                        FROM public.products''')
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no product can be found")
    return posts

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_a_product(post: schemas.Product):
    # post_dict = post.dict()
    # item_id = randrange(1, 5000)
    # if item_id in find_id():
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'post with id {item_id} already existed')
    # else:
    #     post_dict['id'] = item_id
    #     my_posts.append(post_dict)
    cursor.execute('''INSERT INTO 
                        products (name, price, inventory) 
                        VALUES (%s, %s, %s) RETURNING *''',(post.name, post.price, post.inventory))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@router.get("/latest")
def get_recent_product():
    # return {"latest post is": my_posts[-1]}
    cursor.execute('''SELECT * 
                        FROM public.products
                        ORDER BY ID DESC
                        LIMIT 1''')
    latest_product = cursor.fetchone()
    if not latest_product:
        raise Exception(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no product can be found")
    return latest_product

@router.get("/name")
def get_product_by_name(*, category: Optional[int] = None, name: str = Query(None,
                                                                          title='prodname', description='put in the name of product',
                                                                          min_length=2, max_ength=30)):
    # result = []
    # for item in my_posts:
    #     if item['user'] == user:
    #         result.append(item)
    if ',' in name:
        name = tuple(i.lower() for i in name.split(','))
        cursor.execute('''SELECT * 
                        FROM public.products
                        WHERE name IN %s''',(name,))
    else:
        cursor.execute('''SELECT * 
                        FROM public.products
                        WHERE name = lower(%s)''',(name,))
    product_name = cursor.fetchall()
    if product_name:
        return product_name 
    # if len(result) != 0:
    #     return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with name {name} was not found!")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_product(id: int):
    # idx = find_index(id)
    cursor.execute('''DELETE 
                        FROM public.products
                        WHERE id = %s RETURNING *''', (str(id),))
    delete_product = cursor.fetchone()
    # print(delete_product)
    conn.commit()
    # if not idx:
    if not delete_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id {id} was not found!")
    # my_posts.pop(idx)
    return Response(f'product {id} deleted', status_code=status.HTTP_204_NO_CONTENT)

@router.put("/put/{id}")
def update_a_product(id: int, post: schemas.Product):
    cursor.execute('''UPDATE public.products 
                        SET name=%s, price=%s, inventory=%s 
                        WHERE id=%s RETURNING *''', (post.name, post.price, post.inventory, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    # idx = find_index(id)
    # if not idx:
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[idx] = post_dict
    return{f"product {id} updated": updated_post}

@router.patch("/patch/{id}")
def patch_a_product(id: int, post: schemas.Productpatch):
    # idx = find_index(id)
    # print("idx is:", idx)
    # if not idx:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {id} was not found!")
    # stored_data = post.dict()
    # print(stored_data)
    # stored_model = Productpatch(**stored_data)
    # print(stored_model)
    # update_data = post.dict(exclude_unset=True)
    # print(update_data)
    # updated_data = stored_model.copy(update=update_data)
    # post = jsonable_encoder(updated_data)
    # return{"partially updated product": post}
    cursor.execute('''UPDATE public.products 
                        SET name=%s, price=%s, inventory=%s
                        WHERE id=%s RETURNING *''', (post.name, post.price, post.inventory, str(id),))
    updated_product = cursor.fetchone()
    # print(updated_product)
    conn.commit()
    # idx = find_index(id)
    # if not idx:
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id {id} was not found!")
    return{f"product {id} updated": updated_product}

@router.get("/{id}")
def get_a_product(id: int = Path(None, title='Post ID',
                              description='Put in the ID of the product you like to extract', ge=1, le=5000)):
    cursor.execute('''SELECT * 
                        FROM public.products
                        WHERE ID = %s''', (str(id),))
    product = cursor.fetchone()
    # post = find_post(id)
    if not product:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} was not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id {id} was not found!")
    return product