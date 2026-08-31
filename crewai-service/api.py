"""Expose the crew as a REST API endpoint so other services/projects can
trigger it and pull the result, instead of running it via the CLI.

Usage:
    uvicorn api:app --reload --port 8001
"""

from fastapi import FastAPI
from pydantic import BaseModel

from crew import build_crew

app = FastAPI(title="CrewAI Visualization Service")


class KickoffRequest(BaseModel):
    topic: str = "CrewAI Flows"


class KickoffResponse(BaseModel):
    result: str


@app.post("/kickoff", response_model=KickoffResponse)
def kickoff(request: KickoffRequest) -> KickoffResponse:
    crew = build_crew()
    result = crew.kickoff(inputs={"topic": request.topic})
    return KickoffResponse(result=str(result))


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
