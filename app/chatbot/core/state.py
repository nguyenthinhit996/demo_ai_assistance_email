from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

class ChatBotState(TypedDict):
    messages: Annotated[list, add_messages]