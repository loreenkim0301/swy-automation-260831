# LangGraph Visualization Service

코드로 선언한 멀티 에이전트 그래프(Node/Edge)를 Mermaid/PNG로 시각화하고, 로컬 서버로 띄워 REST API로 노출하는 예제입니다.

## 구성

- `agents/state.py` — 에이전트 간 공유 상태 스키마
- `agents/graph.py` — supervisor → researcher/writer 구조의 예시 그래프 (`app`으로 컴파일됨)
- `visualize.py` — `app.get_graph().draw_mermaid_png()`로 그래프를 `graph.png`/`graph.mmd`로 저장
- `langgraph.json` — `langgraph dev`(LangGraph Server/Studio)용 설정
- `mcp_integration.py` — 외부 MCP 서버를 에이전트 도구로 연결하는 예시

## 실행

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY 입력
```

### 1. 그래프 구조 시각화 (LLM 호출 없음)

```bash
python visualize.py
```

`graph.mmd`(Mermaid 소스)와 `graph.png`(렌더링된 이미지)가 생성됩니다. 그래프 구조만 읽으므로 API 키 없이도 동작합니다.

### 2. 로컬 서버로 REST API + Studio 시각화 띄우기

```bash
langgraph dev
```

- REST API: `http://127.0.0.1:2024` (그래프 실행/스트리밍 엔드포인트가 자동 노출됩니다)
- LangGraph Studio: 브라우저에서 에이전트 연결 그래프를 실시간으로 보고, 실행을 단계별로 디버깅할 수 있습니다.

### 3. MCP로 외부 도구 연결

`mcp_integration.py`의 `MCP_SERVERS`를 프로젝트가 이미 노출 중인 MCP 서버 접속 정보로 바꾸면, 해당 서버의 도구를 그대로 에이전트에 연결할 수 있습니다.

```bash
python mcp_integration.py
```

## 원하는 프로젝트에 연결하기

1. `agents/state.py`의 `AgentState`를 프로젝트가 실제로 주고받는 데이터 모양에 맞게 수정합니다.
2. `agents/graph.py`의 세 노드(`supervisor_node`, `researcher_node`, `writer_node`)를 프로젝트의 에이전트 호출 코드로 교체합니다. 노드 수/이름이 달라져도 `add_node`/`add_edge` 구조만 유지하면 `visualize.py`, `langgraph dev`는 그대로 재사용됩니다.
3. 프로젝트가 자체 MCP 서버를 제공한다면 `mcp_integration.py`의 `MCP_SERVERS`만 바꿔서 연결합니다.
