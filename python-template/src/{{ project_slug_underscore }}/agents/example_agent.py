"""Pydantic AI researcher agent with tools attached."""

from pydantic_ai import Agent

from {{ project_slug_underscore }}.config.llm_client import build_llm
from {{ project_slug_underscore }}.config.prompts import RESEARCHER_PROMPT
from {{ project_slug_underscore }}.tools.example_tools import calculator_impl, web_search_impl


def build_researcher() -> Agent:
    agent = Agent(model=build_llm(), system_prompt=RESEARCHER_PROMPT)

    @agent.tool_plain
    def web_search(query: str) -> list[dict]:
        """Search the web (mocked — replace for production)."""
        return web_search_impl(query)

    @agent.tool_plain
    def calculator(expression: str) -> str:
        """Evaluate a safe arithmetic expression."""
        return calculator_impl(expression)

    return agent
