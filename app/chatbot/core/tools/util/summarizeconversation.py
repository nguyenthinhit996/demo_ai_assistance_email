from app.chatbot.core.state import ChatBotState
from langchain_core.messages import HumanMessage, RemoveMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from app.core import config

settings = config.Settings()

llm = ChatOpenAI(model="gpt-4o-mini")


def summarize_conversation_tool(state: ChatBotState):
    # Step 1: Summarize the conversation
    summary = state.get("summary", "")
    if summary:
        # Extend the existing summary
        summary_message = (
            f"This is a summary of the conversation to date: {summary}\n\n"
            "Extend the summary by incorporating the new messages above while ensuring the entire summary does not exceed 1024 characters. Prioritize key points and maintain clarity."
        )
    else:
        # Create a new summary
        summary_message = "Create a summary of the conversation above:"

    # Add the summary request as a new message
    messages = state["messages"] + [HumanMessage(content=summary_message)]

    # Get the summary response from LLM
    response = llm.invoke(messages)

    # Step 2: Retain critical messages
    retained_messages = set()
    for i, message in enumerate(state["messages"]):
        # Keep the last `remaining_last_message` messages
        if i >= len(state["messages"]) - settings.remaining_last_message:
            retained_messages.add(message.id)
            continue

        # Preserve tool-related messages
        if isinstance(message, (AIMessage, ToolMessage)):
            # Retain messages with `tool_calls` or their responses
            if getattr(message, "tool_calls", None) or getattr(message, "tool_call_id", None):
                retained_messages.add(message.id)

    # Step 3: Determine messages to delete
    delete_messages = [
        RemoveMessage(id=message.id)
        for message in state["messages"]
        if message.id not in retained_messages
    ]

    # Step 4: Return updated state
    return {
        "summary": response.content,  # Updated summary
        "messages": delete_messages   # Messages to remove
    }
