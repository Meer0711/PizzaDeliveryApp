from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Settings(BaseModel):
    authjwt_secret_key: str = '84d49609852a658ff36dba90a519d3c51b130841d22b405378a61b3526ce717d'

class LoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str]=None


class OrderModel(BaseModel):
    quantity: int
    pizza_size: Optional[str] = "SMALL"  # Default pizza size
    order_status: Optional[str] = "PENDING"  # Default order status

    class Config:  # Note: Change 'config' to 'Config' (case-sensitive)
        orm_mode = True
        schema_extra = {
            "example": {  # It's a good practice to use 'example' instead of just providing values
                "quantity": 2,
                "pizza_size": "LARGE",
            }
        }

class UserResponse(BaseModel):
    username: str
    email: str
    access_token: str
    token_type: str