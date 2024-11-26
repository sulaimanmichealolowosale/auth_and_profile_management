from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class TokenData(BaseModel):
    id:str
    
    
class RegisterModel(BaseModel):
    username:str = Field(min_length=4, max_length=25)
    email:str
    password:str
    created_at:datetime= datetime.now()
    
class ForgotPassword(BaseModel):
    email:EmailStr
    
class ResetPassword(BaseModel):
    code:str
    email:EmailStr
    password:str
    