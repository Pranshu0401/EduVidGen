from fastapi import APIRouter, Depends, HTTPException, status , Body
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import JWTError, jwt
from auth.authmiddleware import get_current_user
from fastapi.responses import FileResponse
from Model.langchain import generate_and_execute_with_correction
import os
from auth.schemas import UserCreate, Token  , UserLogin , VideoResponse
from auth.dbmodel import User as DBUser , Video          
from database import get_db
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import base64
from supabase import create_client
from typing import List

router = APIRouter()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Signup Route ---

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    new_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
def protected_route(current_user: DBUser = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}. Middleware is working!"}


@router.post("/generatetopic", response_model=VideoResponse)
def generate_topic(
    data: dict = Body(...),
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    topic = data.get("topic")
    if not topic:
        raise HTTPException(status_code=400, detail="Missing topic in request body")

    # Generate video (assuming this creates a temporary file)
    result = generate_and_execute_with_correction(prompt=topic)
    video_path = result.get("video_path")
    
    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Generated video not found")

    # Upload to Supabase Storage
    file_key = f"users/{current_user.id}/videos/{os.path.basename(video_path)}"
    
    supabase.storage.from_("videos").upload(file_key, video_path,
                                            {"content-type" : "video/mp4"})
    # Store metadata in DB
    video_record = Video(
        title=topic,
        scene_plan=result['plan'],
        manim_code=result['final_code'],
        video_path=file_key,  # Store path instead of binary
        owner=current_user
    )
    db.add(video_record)
    db.commit()

    video_url = supabase.storage.from_("videos").get_public_url(file_key)

    return {
        "title": topic,
        "scene_plan": result['plan'],
        "video_url": video_url,
        "manim_code": result['final_code']
    }


@router.get("/myvideos", response_model=List[VideoResponse])
def get_user_videos(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    videos = db.query(Video).filter(Video.user_id == current_user.id).all()
    
    response = []
    for video in videos:
        # Generate signed URL (expires in 1 hour)
        signed_url = supabase.storage.from_("videos").get_public_url(video.video_path)
        
        response.append({
            "title": video.title,
            "scene_plan": video.scene_plan,
            "video_url": signed_url,
            "manim_code": video.manim_code
        })
    
    return response


