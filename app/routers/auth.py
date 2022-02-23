from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import verify
from ..oauth import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. schemas import UserLogin, Token
from .. models import User

router = APIRouter(tags = ["Authentication"])


@router.post("/login", response_model=Token )
def login(login_cred : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_details = db.query(User).filter(User.email == login_cred.username).first()

    if not user_details:
       raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid credentials")

    if not verify(login_cred.password, user_details.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid credentials")

    token =  create_access_token(data= {"user_id": user_details.id})
    return {"access_token": token, "token_type": "bearer"}

    

