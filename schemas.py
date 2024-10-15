from pydantic import BaseModel
from typing import Optional


from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupModel(BaseModel):
    id: Optional[int]  # Optional, can be omitted in signup requests
    username: str
    email: EmailStr  # Use EmailStr for email validation
    password: str
    is_staff: Optional[bool] = False  # Set default to False
    is_active: Optional[bool] = True  # Set default to True

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "securepassword",
                "is_staff": False,
                "is_active": True
            }
        }

