from pathlib import Path

from app.agent import ToolUsingAgent
from app.evaluation import EvalCase, tool_selection_accuracy
from app.tools import CSVSummaryTool, CalculatorTool, TextSearchTool


def make_agent(tmp_path: Path) -> ToolUsingAgent:
    corpus = tmp_path / "knowledge"
    corpus.mkdir()
    (corpus / "facts.txt").write_text(
        "Express shipping takes two days.\nRefunds are available for 30 days.",
        encoding="utf-8",
    )
    return ToolUsingAgent(
        tools=[
            CalculatorTool(),
            TextSearchTool(corpus_dir=corpus),
            CSVSummaryTool(),
        ]
    )


def test_calculator_and_memory(tmp_path):
    agent = make_agent(tmp_path)
    result = agent.run("calculate: 12 * 4 + 2", "s1")
    assert result.response == "50"
    assert result.tool_used == "calculator"
    assert len(agent.memory.get("s1")) == 2


def test_search_tool(tmp_path):
    agent = make_agent(tmp_path)
    result = agent.run("search: express shipping")
    assert "facts.txt" in result.response
    assert result.tool_used == "text_search"


def test_guardrail(tmp_path):
    agent = make_agent(tmp_path)
    result = agent.run("")
    assert result.tool_used is None
    assert result.response.startswith("Request blocked:")


def test_tool_selection_accuracy(tmp_path):
    agent = make_agent(tmp_path)
    cases = [
        EvalCase("calculate: 2 + 2", "calculator"),
        EvalCase("search: refunds", "text_search"),
        EvalCase("hello there", None),
    ]
    assert tool_selection_accuracy(agent, cases) == 1.0
