from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class LLMstate(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]
    