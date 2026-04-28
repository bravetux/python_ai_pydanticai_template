"""Pydantic AI tool helpers — registered on the agent in agents/example_agent.py."""

import ast
import operator
from typing import Any

_MOCK_RESULTS = [
    {"title": "Tokyo - Wikipedia", "url": "https://en.wikipedia.org/wiki/Tokyo",
     "snippet": "Tokyo is the capital of Japan with a population of approximately 13,960,000 (2024)."},
    {"title": "Tokyo Statistics", "url": "https://www.metro.tokyo.lg.jp/english/about/",
     "snippet": "As of 2024, Greater Tokyo has 13.96 million residents."},
    {"title": "World Population Review — Tokyo",
     "url": "https://worldpopulationreview.com/world-cities/tokyo-population",
     "snippet": "Tokyo's 2024 population: 13,960,000."},
]

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
    ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsupported node: {type(node).__name__}")


def web_search_impl(query: str) -> list[dict[str, Any]]:
    return _MOCK_RESULTS


def calculator_impl(expression: str) -> str:
    return str(_eval(ast.parse(expression, mode="eval").body))
