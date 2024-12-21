from ..database import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_check = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)

    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has already vote on the post")
        new_votes = models.Vote(post_id = vote.post_id, user_id = curr_user.id)
        db.add(new_votes)
        db.commit()

        return {"message": "vote successfully added"}

    elif vote.dir == 0:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "vote successfully removed"}
        
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invlid vote direction")