from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):
    APPROVAL = "approval"
    EDIT = "edit"
    FEEDBACK = "feedback"


class UserMessage(BaseModel):
    """
    Schema message for user can asking.
    """
    threadId: int = Field(..., min=1, example=1, title="Thread ID", description="Unique identifier for the conversation thread.")
    msg: str = Field(..., min_length=1, example="Hello AI!", title="User Message", description="The content of the user's message.")
    status: Optional[StatusEnum] = Field(default=None, example="approval", title="Message Status", description="Current status of the message.")