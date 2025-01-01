from pydantic import BaseModel, Field

class UserMessage(BaseModel):
    """
    Schema message for user can asking.
    """
    threadId: int = Field(..., min=1, example=1)
    msg: str = Field(..., min_length=1, example="Hello AI!")