from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from .. import models, schemas
from app.database import get_db
from typing import Optional, List
import copy

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * from posts""")
    # posts = cursor.fetchall()
    print(limit)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)

    posts_votes = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    # print(posts_votes)

    return posts_votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # f-string is not used here because that could lead to SQL Injection
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # above code is equivalent to  staging

    # # below line commits the change
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(author_id=current_user.id,
                           **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # equilent to RETURNING as in raw SQL

    '''
    Here new_post is a sqlalchemy model, Pydantic can understand dict, for pydantic to understand sqlalchemy ORM,
    we add 

    class Config:
        orm_mode = True

    in PostResponse Class in schemas.py. 
    
    If we were to return only post in below line, then this part of code is not requried
    '''
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('SELECT * FROM posts WHERE id= %s', (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)  -> before introducing database concept
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id : {id} does not exist')

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('DELETE FROM posts WHERE id= %s returning *', (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id : {id} does not exist')

    post_to_be_deleted = copy.deepcopy(post_query.first())
    ''' deepcopy is used because the contents of post to be deleted are copied to post_to_be_deleted in a different location.
        if normal assignemnt is used here, then post_to_be_deleted will be null, once the post is deleted from the database.
    '''
    if post_to_be_deleted.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': f'Post with id : {id} successfully deleted', 'deleted_post': post_to_be_deleted}


@router.put("/{id}", response_model=schemas.PostResponse)
def udpate_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %sreturning *''',
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id : {id} does not exist')

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


# @router.patch("/update_post_patch/{id}")
# def update_post_patch(id: int, title: str):
#     index = find_post_index(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'Post with id : {id} does not exist')
#     my_posts[index]['title'] = title
#     return {'updated_post': my_posts[index]}
