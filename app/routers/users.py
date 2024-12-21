from ..database import get_db
from fastapi import Response, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Email is already registered")

    user.password = utils.hash_password(user.password)
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()

    db.refresh(user) 
    return user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exists")
    return user

