"""Example: expose an external MCP server's tools to one of the graph's
agents, and (separately) expose this graph itself as an MCP-compatible
tool source for other clients.

Point `MCP_SERVERS` at the MCP server(s) your project already runs (e.g.
a filesystem server, a project-specific tool server) and the researcher
agent below will be able to call their tools directly — no rewrite of
agents/graph.py needed, just swap that node's `llm.invoke` for the
tool-calling agent built here.
"""

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from agents.graph import llm

# Replace with your own project's MCP server(s).
MCP_SERVERS = {
    "project_tools": {
        # stdio example: a local MCP server started as a subprocess
        "command": "python",
        "args": ["-m", "your_project.mcp_server"],
        "transport": "stdio",
    },
    # "project_api": {
    #     # streamable-http example: an already-running MCP server
    #     "url": "http://localhost:8000/mcp",
    #     "transport": "streamable_http",
    # },
}


async def build_mcp_researcher():
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    return create_react_agent(llm, tools)


async def main() -> None:
    agent = await build_mcp_researcher()
    result = await agent.ainvoke({"messages": [("user", "List the tools you have access to.")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
