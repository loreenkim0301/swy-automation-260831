"""Example: attach an external MCP server's tools to a CrewAI agent.

Point `SERVER_PARAMS` at the MCP server your project already runs (e.g.
a filesystem server, a project-specific tool server) and the agent below
will be able to call its tools directly.
"""

from crewai import Agent, Crew, Task
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

# Replace with your own project's MCP server.
SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "your_project.mcp_server"],
)

# streamable-http alternative for an already-running MCP server:
# SERVER_PARAMS = {"url": "http://localhost:8000/mcp", "transport": "streamable-http"}

if __name__ == "__main__":
    with MCPServerAdapter(SERVER_PARAMS) as mcp_tools:
        print(f"Available MCP tools: {[tool.name for tool in mcp_tools]}")

        agent = Agent(
            role="MCP-connected Researcher",
            goal="Use the connected MCP tools to answer the user's request",
            backstory="An analyst who relies on the project's own MCP tools instead of general knowledge.",
            tools=mcp_tools,
            verbose=True,
        )

        task = Task(
            description="List the tools you have access to and what each one does.",
            expected_output="A bullet list of available tools and their purpose.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task])
        print(crew.kickoff())
