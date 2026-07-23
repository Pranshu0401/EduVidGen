from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- Video Schemas (Now Storage-Friendly) ---

class VideoBase(BaseModel):
    title: str  # Added title field which was in your router but missing in schemas
    scene_plan: Optional[str] = None
    manim_code: Optional[str] = None
    video_path: Optional[str] = None  # Stores path in Supabase Storage instead of bytes

class VideoCreate(VideoBase):
    """For video creation (accepts file upload)"""
    pass  # File handling will be done in the endpoint, not via schema

class VideoResponse(VideoBase):
    """Response model with URL instead of binary data"""
    manim_code : str
    video_url: HttpUrl  # URL to access the video
    scene_plan : str
    title : str


    class Config:
        orm_mode = True

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    """Response model (never returns password)"""
    id: int
    created_at: datetime
    videos: List[VideoResponse] = []  # Now returns VideoResponse instead of Video

    class Config:
        orm_mode = True

# --- Auth Token Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None