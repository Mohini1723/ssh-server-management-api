from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    profile_photo: Optional[str] = None  
    
class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    profile_photo: Optional[str] = None


class ServerBase(BaseModel):
    name: str
    ip_address: str
    username: str
    port: int = 22
    status: str = "active"

class ServerCreate(ServerBase):
    password: Optional[str] = None
    ssh_private_key: Optional[str] = None

class ServerUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    username: Optional[str] = None
    port: Optional[int] = None
    password: Optional[str] = None
    ssh_private_key: Optional[str] = None
    status: Optional[str] = None

class ServerResponse(ServerBase):
    id: str
    owner_email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CommandRequest(BaseModel):
    command: str
