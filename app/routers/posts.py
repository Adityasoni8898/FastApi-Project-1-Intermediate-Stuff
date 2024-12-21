from ..database import get_db
from fastapi import Response, Depends, HTTPException, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/post",
    tags=['Post']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_all_post(db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).offset(skip).limit(limit).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_all_post(id:int, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exists")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    post = models.Post(user_id = curr_user.id, **post.model_dump())
    
    db.add(post)
    db.commit()

    db.refresh(post) # puts the most recently added value into var post
    return post

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def get_all_post(id:int, post:schemas.CreatePost, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first() 

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exists")
    
    if curr_user.id != post_query.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return updated_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_all_post(id:int, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exists")
    
    if curr_user.id != post_query.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)