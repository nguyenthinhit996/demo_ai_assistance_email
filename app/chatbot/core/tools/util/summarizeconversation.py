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
        # If a summary exists, extend it
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by incorporating the new messages above while ensuring the entire summary does not exceed 1024 characters. Prioritize key points and maintain clarity."
        )
    else:
        # Create a new summary
        summary_message = "Create a summary of the conversation above:"

    # Add summary request to the conversation
    messages = state["messages"] + [HumanMessage(content=summary_message)]

    # Get summary response from LLM
    response = llm.invoke(messages)

    # Step 2: Identify messages to retain
    retained_messages = []
    for i, message in enumerate(state["messages"]):
        # Keep the last `remaining_last_message` messages
        if i >= len(state["messages"]) - settings.remaining_last_message:
            retained_messages.append(message)
            continue

        # Preserve messages with tool_calls or their dependencies
        if isinstance(message, (ToolMessage, AIMessage)) and getattr(message, "tool_calls", None):
            retained_messages.append(message)
            continue

    # Step 3: Remove all other messages
    delete_messages = [
        RemoveMessage(id=m.id) for m in state["messages"] if m not in retained_messages
    ]

    # Step 4: Return updated state
    return {
        "summary": response.content,  # The updated conversation summary
        "messages": delete_messages   # Messages to remove from the state
    }
