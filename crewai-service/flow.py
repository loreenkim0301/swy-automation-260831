"""Example CrewAI Flow: wires the researcher and writer crew into an
explicit sequence of steps and renders an interactive dependency graph.

Usage:
    python flow.py

Renders an interactive HTML dependency graph and copies it (plus its
css/js) into ./crew_flow/ — open crew_flow/crew_flow.html in a browser to
see which step depends on which, and the order they run in.
"""

import shutil
from pathlib import Path

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from crew import researcher, writer


class VisualizationFlowState(BaseModel):
    topic: str = "CrewAI Flows"
    research_notes: str = ""
    summary: str = ""


class VisualizationFlow(Flow[VisualizationFlowState]):
    @start()
    def research(self):
        result = researcher.kickoff(f"Research {self.state.topic} and list the key facts.")
        self.state.research_notes = str(result)
        return self.state.research_notes

    @listen(research)
    def write(self, research_notes: str):
        result = writer.kickoff(
            f"Using these findings, write a short summary of {self.state.topic}:\n{research_notes}"
        )
        self.state.summary = str(result)
        return self.state.summary


if __name__ == "__main__":
    flow = VisualizationFlow()

    # plot() always renders into a temp directory and returns the absolute
    # path to the HTML file there; copy the whole directory locally so the
    # visualization (html + css + js) is self-contained and easy to find.
    generated_path = Path(flow.plot("crew_flow.html", show=False))
    output_dir = Path("crew_flow")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(generated_path.parent, output_dir)
    print(f"Wrote {output_dir / generated_path.name}")

    result = flow.kickoff()
    print(result)
