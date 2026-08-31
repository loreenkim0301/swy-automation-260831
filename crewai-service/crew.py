"""Example role-based crew: a researcher gathers facts, a writer turns
them into a final answer.

Replace the Agent/Task definitions below with your own project's roles
to visualize *their* interconnections instead of this example.
"""

from crewai import Agent, Crew, Process, Task

researcher = Agent(
    role="Researcher",
    goal="Gather accurate, well-sourced facts about {topic}",
    backstory="An analyst who finds and verifies information before anyone writes about it.",
    verbose=True,
)

writer = Agent(
    role="Writer",
    goal="Turn research about {topic} into a clear, concise final answer",
    backstory="A writer who turns raw findings into something a reader can act on.",
    verbose=True,
)

research_task = Task(
    description="Research {topic} and list the key facts a reader needs to know.",
    expected_output="A bullet list of key facts about {topic}.",
    agent=researcher,
)

writing_task = Task(
    description="Using the research findings, write a short, clear summary of {topic}.",
    expected_output="A 3-5 sentence summary of {topic}.",
    agent=writer,
    context=[research_task],
)


def build_crew() -> Crew:
    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    crew = build_crew()
    result = crew.kickoff(inputs={"topic": "CrewAI Flows"})
    print(result)
