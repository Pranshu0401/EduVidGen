from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwtToken import verify_access_token
from auth.dbmodel import User as DBUser            # Your actual DB model
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # or your token URL

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)   # Add DB session
) -> DBUser:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
