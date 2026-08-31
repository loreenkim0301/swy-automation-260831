# CrewAI Visualization Service

역할 기반(Role-based) 에이전트를 코드로 선언하고, 이들의 실행 순서/의존관계를 인터랙티브 그래프로 시각화하며, REST API로 배포하는 예제입니다.

## 구성

- `crew.py` — 예시 Agent(Researcher, Writer) + Task + `Crew` 정의
- `flow.py` — 위 Crew를 단계(`@start`/`@listen`)로 오케스트레이션하는 `Flow`, `flow.plot()`으로 의존 그래프를 HTML로 저장
- `api.py` — Crew를 REST API 엔드포인트(`POST /kickoff`)로 노출하는 FastAPI 앱
- `mcp_tool_example.py` — 외부 MCP 서버를 에이전트 도구로 연결하는 예시

## 실행

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY 입력
```

### 1. Flow 시각화

```bash
python flow.py
```

`crew_flow/crew_flow.html`이 생성됩니다. 브라우저로 열면 어떤 단계가 어떤 단계에 의존하는지, 실행 순서가 어떻게 되는지 그래프로 보여줍니다. (동시에 Crew를 실제로 한 번 실행합니다.)

### 2. REST API로 배포

```bash
uvicorn api:app --reload --port 8001
```

```bash
curl -X POST http://localhost:8001/kickoff -H "Content-Type: application/json" -d '{"topic": "멀티 에이전트 오케스트레이션"}'
```

### 3. MCP로 외부 도구 연결

`mcp_tool_example.py`의 `SERVER_PARAMS`를 프로젝트가 이미 노출 중인 MCP 서버 접속 정보로 바꾸면, 해당 서버의 도구를 그대로 에이전트에 연결할 수 있습니다.

```bash
python mcp_tool_example.py
```

## 원하는 프로젝트에 연결하기

1. `crew.py`의 `Agent`/`Task` 정의를 프로젝트의 실제 역할로 교체합니다.
2. `flow.py`의 `@start`/`@listen` 단계를 프로젝트의 실행 순서에 맞게 재구성합니다. 단계를 추가/삭제해도 `flow.plot()`은 그대로 재사용됩니다.
3. 프로젝트가 자체 MCP 서버를 제공한다면 `mcp_tool_example.py`의 `SERVER_PARAMS`만 바꿔서 연결합니다.
