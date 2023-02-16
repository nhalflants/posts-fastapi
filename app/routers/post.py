from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import app.models as models
import app.database as db
import app.schemas as schemas
import app.oauth2 as oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model=List[schemas.PostVote])
def get_posts(
    db: Session = Depends(db.get_db), 
    user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10, 
    offset: int = 0, 
    search: Optional[str] = ""):

    # Filter posts created by logged in user
    # posts = db.query(models.Post).filter(models.Post.user_id == user.id).all()
    
    # posts = db.query(models.Post)\
    #     .filter(models.Post.title.contains(search))\
    #     .limit(limit)\
    #     .offset(offset).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(offset)\
        .all()

    return results


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostRequest, 
    db: Session = Depends(db.get_db),
    user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(db.get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id {id} is not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(db.get_db), user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id {id} is not found")
    
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostRequest, db: Session = Depends(db.get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id {id} is not found")

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post.update(post.dict(), synchronize_session=False)
    db.commit()

    return post