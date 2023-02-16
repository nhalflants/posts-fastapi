from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import app.models as models
import app.database as db
import app.schemas as schemas
import app.oauth2 as oauth2

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_vote(
    posted_vote: schemas.Vote, 
    db: Session = Depends(db.get_db), 
    user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == posted_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {posted_vote.post_id} doesn't exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == posted_vote.post_id, models.Vote.user_id == user.id)
    vote = vote_query.first()

    if posted_vote.dir == 1:
        if vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user.id} has already voted for post {vote.post_id}")
        
        new_vote = models.Vote(post_id=posted_vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
    
    else:
        if not vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesn't exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}