"""Example multi-agent graph: a supervisor routes work between a
researcher and a writer agent until the task is done.

Replace the three node functions below with calls into your own project's
agents to visualize *their* interconnections instead of this example.
"""

from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from agents.state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

MEMBERS = ["researcher", "writer"]


class Route(BaseModel):
    next: Literal["researcher", "writer", "FINISH"]


SUPERVISOR_PROMPT = (
    "You are a supervisor coordinating a researcher and a writer agent to "
    "answer the user's request. Given the conversation so far, decide who "
    "should act next, or FINISH if the request has been fully answered."
)


def supervisor_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=SUPERVISOR_PROMPT)] + state["messages"]
    route = llm.with_structured_output(Route).invoke(messages)
    return {"next": route.next}


def researcher_node(state: AgentState) -> dict:
    messages = [
        SystemMessage(content="You are a researcher. Gather the facts needed to answer the request.")
    ] + state["messages"]
    result = llm.invoke(messages)
    return {"messages": [result]}


def writer_node(state: AgentState) -> dict:
    messages = [
        SystemMessage(content="You are a writer. Turn the research so far into a clear final answer.")
    ] + state["messages"]
    result = llm.invoke(messages)
    return {"messages": [result]}


def route_from_supervisor(state: AgentState) -> str:
    return END if state["next"] == "FINISH" else state["next"]


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"researcher": "researcher", "writer": "writer", END: END},
    )
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")

    return graph


app = build_graph().compile()

if __name__ == "__main__":
    for event in app.stream({"messages": [HumanMessage(content="Summarize what LangGraph is used for.")]}):
        print(event)
