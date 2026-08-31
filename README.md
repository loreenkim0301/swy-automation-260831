# Multi-Agent Visualization Sandbox

두 개의 대표적인 코드 기반 멀티 에이전트 프레임워크를 로컬에 띄워두고, 원하는 프로젝트의 에이전트를 연결해 상호작용(그래프/흐름)을 시각화 테스트하기 위한 샌드박스입니다.

| | [`langgraph-service/`](./langgraph-service) | [`crewai-service/`](./crewai-service) |
|---|---|---|
| 성격 | Graph 기반 (Node/Edge를 코드로 선언) | Role 기반 (Agent/Task/Crew, Flow로 오케스트레이션) |
| 시각화 | `app.get_graph().draw_mermaid_png()` → Mermaid/PNG | `flow.plot()` → 인터랙티브 HTML 의존성 그래프 |
| 로컬 서버 | `langgraph dev` → REST API + LangGraph Studio | FastAPI 래퍼(`api.py`) → REST API |
| MCP 연동 | `langchain-mcp-adapters`로 MCP 서버를 도구로 로드 | `crewai-tools`의 `MCPServerAdapter`로 MCP 서버를 도구로 로드 |
| 비용 | 무료/오픈소스 (LLM 호출 비용은 별도) | 무료/오픈소스 (LLM 호출 비용은 별도) |

## 빠른 시작

각 서비스는 독립적으로 동작하며, 자체 `requirements.txt`와 `README.md`를 가지고 있습니다.

```bash
# LangGraph
cd langgraph-service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY 입력
python visualize.py    # graph.png / graph.mmd 생성
langgraph dev          # REST API + Studio 시각화

# CrewAI
cd crewai-service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY 입력
python flow.py          # crew_flow.html 생성 (브라우저로 확인)
uvicorn api:app --reload --port 8001   # REST API로 배포
```

## 원하는 프로젝트에 연결하기

두 서비스 모두 "예시 에이전트"만 들어있는 템플릿입니다. 실제로 시각화하고 싶은 프로젝트가 있다면:

1. **LangGraph**: `langgraph-service/agents/graph.py`의 노드 함수들을 프로젝트의 에이전트 호출 코드로 교체하고, `agents/state.py`의 상태 스키마를 프로젝트에 맞게 조정합니다. 노드/엣지 구조만 유지하면 `visualize.py`와 `langgraph dev`는 그대로 재사용됩니다.
2. **CrewAI**: `crewai-service/crew.py`의 `Agent`/`Task` 정의를 프로젝트의 역할로 교체하고, `flow.py`의 `@start`/`@listen` 단계를 프로젝트의 실행 순서에 맞게 재구성합니다.

각 서비스 폴더의 `mcp_integration.py` / `mcp_tool_example.py`는 외부 MCP 서버(예: 프로젝트가 이미 노출하고 있는 MCP 서버)를 에이전트의 도구로 그대로 연결하는 예시입니다. 프로젝트가 MCP 서버를 제공한다면 코드 재작성 없이 이 파일의 서버 접속 정보만 바꿔서 연결할 수 있습니다.
