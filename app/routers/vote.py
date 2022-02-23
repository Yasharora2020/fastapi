from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. schemas import Votes
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth import get_current_user
from ..models import VoteTable, Post





router = APIRouter(prefix = "/vote", tags = ['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : Votes, db: Session = Depends(get_db), current_user:int = Depends(get_current_user)):

    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")
                            
    vote_query = db.query(VoteTable).filter(VoteTable.post_id == vote.post_id, VoteTable.user_id == current_user.id )
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User{current_user.id} has already voted on post {vote.post_id}")
        new_vote = VoteTable(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message " : " successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "Successfully deleted Vote" }
    

