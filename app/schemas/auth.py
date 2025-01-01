from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    """
    Schema for user creation and login.
    """
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    password: str = Field(..., min_length=6, example="securepassword123")

class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str
