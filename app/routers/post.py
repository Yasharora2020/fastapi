from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. schemas import PostBase, UserCreate, PostCreate, PostResponse, UserResponse,PostOut
from .. import models
from ..oauth import get_current_user
from sqlalchemy import func


router = APIRouter(prefix = "/posts", tags= ["Posts"],)

@router.get("/" ,response_model = List[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip : int=0, search: Optional[str] = ""):
    #using sql alchemy which automatically generates a SQL query
    #posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.VoteTable.post_id).label("votes")).join(models.VoteTable, models.VoteTable.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
  
    return posts

    #  below creates a connection to DB using psycopg2 and then we write sql query
    #cursor.execute(""" SELECT * FROM post""")
    #posts = cursor.fetchall()
    #return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = PostResponse)
def create_posts(post : PostCreate, db: Session = Depends(get_db), current_user :int = Depends(get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    #new_post = models.Post(owner_id = current_user.id, title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
    
    #post_dict= post.dict()
    #post_dict['id'] = randrange(0,1000000000)
    #my_posts.append(post_dict)
    #return {"data": post_dict}
    #  below creates a connection to DB using psycopg2 and then we write sql query
    #cursor.execute(""" INSERT INTO post(title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #return new_post



@router.get("/{id}", response_model = PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user :int = Depends(get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post, func.count(models.VoteTable.post_id).label("votes")).join(models.VoteTable, models.VoteTable.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} not found")
    return post


    
    
    # post = find_posts(int(id))
    #if not post:
    #    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} not found")
    
    #return {"post_detail": post}
    #cursor.execute(""" SELECT * FROM post WHERE id =%s """, (str(id)))
    #post = cursor.fetchone()
    #if not post:
    #   raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} not found")
    #return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id : int, db: Session = Depends(get_db), current_user :int = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #index = find_index_posts(id)
    #my_posts.pop(index)
    #return {'message' : "post was deleted"}
    #cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
    #deleted_posts = cursor.fetchone()
    #conn.commit()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f" not found{id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not Authorised")

    post_query.delete(synchronize_session=False)
    db.commit()

    #my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = PostResponse)
def update_posts(id : int , updated_post : PostCreate, db: Session = Depends(get_db), current_user :int = Depends(get_current_user)):
    #cursor.execute(""" UPDATE post SET title = %s, content = %s,published = %s where id = %s RETURNING * """,(post.title, post.content, post.published, str(id)) )
    #updated_posts= cursor.fetchone()
    #conn.commit()
    #index = find_index_posts(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"not found{id}")
    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not Authorised")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    #post_dict= post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return post_query.first() 
