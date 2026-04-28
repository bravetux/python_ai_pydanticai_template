# Python AI Pydantic AI Agent Template (`python_ai_pydanticai_template`)

A Copier template for bootstrapping production-ready AI agent projects using [Pydantic AI](https://ai.pydantic.dev/), with Anthropic / Bedrock / OpenAI provider support, a Streamlit chat UI, and a modern Python toolchain: `uv`, `ruff`, tests, docs, Docker, and releases.

## Why this template
- Start fast with a **type-safe Agent + tool-registered-on-agent** architecture out of the box.
- Includes working examples of `Agent`, `agent.tool_plain`, structured outputs, and `run_sync`.
- Streamlit chat UI with session management ready to go.
- Provider-agnostic — flip `LLM_PROVIDER` between Anthropic API, AWS Bedrock, and OpenAI without code changes.
- Keep quality automated with linting, formatting, type checking, and tests.

## Technology stack
- [Pydantic AI](https://ai.pydantic.dev/) for type-safe, model-agnostic agents (loved by FastAPI / Pydantic users).
- [Streamlit](https://streamlit.io/) for the web chat UI.
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for typed configuration.
- [Copier](https://copier.readthedocs.io/), [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), `pre-commit`, `pytest`, [MkDocs](https://www.mkdocs.org/) Material, [Docker](https://www.docker.com/).
- `AGENTS.md.jinja` to generate a project-specific `AGENTS.md`.

## Usage

```bash
uvx copier copy Template/python_ai_pydanticai_template my_first_agent \
  --data package_name=my_first_agent \
  --data project_description="My first agent" \
  --data github_username=YOU
```

## Quick start

### 1. Install [`uv`](https://github.com/astral-sh/uv)

### 2. Create the project using copier

```bash
uvx copier copy <path-to>/python_ai_pydanticai_template my-pydanticai-agent
```

| Prompt | Description |
|--------|-------------|
| `package_name` | Name of the Python AI agent package |
| `project_description` | Short description of the project |
| `github_username` | GitHub username or organization name |

> [!IMPORTANT]
> Copier always generates a `.copier-answers.yml`. Commit it; never edit manually.

### 3. Setup

```bash
cd my-pydanticai-agent
git init --initial-branch=main
cp .env.example .env
# Edit .env — set ANTHROPIC_API_KEY (default provider is anthropic)
make install
git add . && git commit -m "feat: first commit"
```

### 4. Run the agent

```bash
make run     # CLI single query
make repl    # CLI interactive REPL
make ui      # Streamlit UI
```

## Generated project structure

```
your-project/
├── app.py                              # Streamlit chat UI entry point
├── main.py                             # CLI entry point
├── pyproject.toml
├── Makefile
├── .env.example
├── AGENTS.md
├── src/<package>/
│   ├── config/
│   │   ├── settings.py                 # pydantic-settings
│   │   ├── llm_client.py               # AnthropicModel / BedrockConverseModel / OpenAIModel
│   │   └── prompts.py
│   ├── agents/
│   │   ├── orchestrator.py             # researcher.run_sync wrapper
│   │   └── example_agent.py            # Agent(...) with @agent.tool_plain registration
│   ├── tools/
│   │   └── example_tools.py            # web_search_impl + calculator_impl helpers
│   └── ui/
│       └── components.py
├── tests/
│   ├── conftest.py
│   ├── test_example_tools.py           # Tests against *_impl helpers
│   └── test_settings.py
├── docker/
├── docs/
├── scripts/
└── playground/notebook.py
```

## Architecture

```
User Query
    │
    ▼
┌────────────────────┐
│   Orchestrator      │  ← researcher.run_sync(query)
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│   Researcher        │  ← Agent(model, system_prompt) + @agent.tool_plain
│   (Pydantic Agent)  │
└──┬──────────────┬──┘
   │              │
   ▼              ▼
┌────────┐  ┌────────────┐
│ web_   │  │ calculator │   ← *_impl plain functions, registered on the agent
│ search │  │            │
└────────┘  └────────────┘
```

### Key patterns

- **Tools registered on the agent** — Pydantic AI uses `@agent.tool_plain` (or `@agent.tool` for context-aware tools). Tools live as plain `*_impl` helpers in `tools/` and are wrapped at agent-construction time.
- **Type-safe outputs** — pass `output_type=MyModel` to `Agent(...)` to get parsed, validated results.
- **`run_sync` / `run` / `run_stream`** — three ways to invoke the agent. The template uses `run_sync` for simplicity.
- **Provider switching** — `config/llm_client.py:build_llm()` returns `AnthropicModel`, `BedrockConverseModel`, or `OpenAIModel`.
- **Configuration** — `pydantic-settings` loads from `.env`.

## Adding a new sub-agent

1. **Create tool helpers** in `src/<package>/tools/my_tools.py`:

   ```python
   def fetch_data_impl(query: str) -> dict:
       return {"result": "..."}
   ```

2. **Create agent** in `src/<package>/agents/my_agent.py`:

   ```python
   from pydantic_ai import Agent
   from <package>.config.llm_client import build_llm
   from <package>.tools.my_tools import fetch_data_impl

   def build_my_agent() -> Agent:
       agent = Agent(model=build_llm(), system_prompt="You are a specialist agent for ...")

       @agent.tool_plain
       def fetch_data(query: str) -> dict:
           """Fetch data for the given query."""
           return fetch_data_impl(query)

       return agent
   ```

3. **Compose in orchestrator** — call multiple agents in sequence:

   ```python
   def build_orchestrator():
       researcher = build_researcher()
       fetcher = build_my_agent()
       def run(query):
           a = researcher.run_sync(query).output
           b = fetcher.run_sync(f"Fetch related data for: {a}").output
           return f"{a}\n\n{b}"
       return run
   ```

4. **Write tests** in `tests/test_my_tools.py`:

   ```python
   def test_fetch():
       assert "result" in fetch_data_impl("foo")
   ```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `anthropic` | One of `anthropic`, `bedrock`, `openai` |
| `ANTHROPIC_API_KEY` | | Required when `LLM_PROVIDER=anthropic` |
| `MODEL_ID` | `claude-sonnet-4-6` | Anthropic / Bedrock model ID |
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |
| `BEDROCK_MODEL_ID` | `anthropic.claude-sonnet-4-6-v1:0` | Bedrock model ID |
| `OPENAI_API_KEY` | | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL_ID` | `gpt-4o-mini` | OpenAI model ID |
| `MAX_TOKENS` | `2048` | Max response tokens |
| `TEMPERATURE` | `0.7` | LLM temperature |
| `LOG_LEVEL` | `INFO` | Logging level |

## Makefile commands

| Command | Description |
|---------|-------------|
| `make install` | Installs dependencies and pre-commit hooks |
| `make run` | CLI: runs the default query |
| `make repl` | CLI: REPL |
| `make ui` | Streamlit UI |
| `make test` | pytest |
| `make lint` | Ruff |
| `make typecheck` | `ty` |
| `make format` | Ruff format |
| `make docs` | MkDocs serve |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run container |
| `make clean` | Clean caches |

## Documentation

```bash
make docs
```

## Update an existing project

```bash
uvx copier update --defaults
```
