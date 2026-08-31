"""Shared state schema for the example multi-agent graph.

Swap this out for your own project's state shape when you connect real
agents — the rest of the graph only relies on `messages` and `next`.
"""

from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: Literal["researcher", "writer", "FINISH"]
