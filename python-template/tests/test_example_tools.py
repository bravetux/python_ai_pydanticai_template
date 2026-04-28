"""Pydantic AI tool tests. Underlying functions exposed as `*_impl`."""

from {{ project_slug_underscore }}.tools.example_tools import calculator_impl, web_search_impl


def test_web_search_returns_three_mock_results() -> None:
    assert len(web_search_impl("Tokyo")) == 3


def test_calculator_basic_arithmetic() -> None:
    assert calculator_impl("13960000 / 1000") == "13960.0"


def test_calculator_rejects_unsafe_expression() -> None:
    import pytest
    with pytest.raises(Exception):
        calculator_impl("__import__('os').system('echo pwned')")
