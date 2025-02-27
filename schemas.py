from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    is_superuser: bool
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool
    
class Login(BaseModel):
	username: str
	password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_superuser: Optional[bool] = None

class BiasRequest(BaseModel):
    text: str
    bias_level: dict
    
class TextRequest(BaseModel):
    text: str

class NeuReason(BaseModel):
    text: str
    image_path: str
    # bias_level: str