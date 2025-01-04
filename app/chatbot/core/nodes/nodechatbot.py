
from app.chatbot.core.state import ChatBotState
from langchain_openai import ChatOpenAI
from app.chatbot.core.nodes.nodetools import node_run_tool
from app.core import config

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from datetime import date, datetime



import logging
logger = logging.getLogger(__name__)


#  # Create a settings instance
settings = config.Settings()


assistant_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful customer support assistant for Resvu."
                    "Resvu is a single-platform customer service solution that revolutionises the way management companies connect with their communities."
                    "\nCurrent time: {time}.",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now)

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = assistant_prompt | llm.bind_tools(node_run_tool)

# def node_call_llm(state: ChatBotState):
#     return {"messages": [llm_with_tools.invoke(state["messages"])]}

class Assistant:
    def __init__(self):
        self.runnable = llm_with_tools

    def __call__(self, state: ChatBotState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}