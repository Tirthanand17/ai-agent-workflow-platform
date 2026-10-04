from __future__ import annotations

import ast
import operator as op
from dataclasses import dataclass
from pathlib import Path
import pandas as pd


class ToolError(ValueError):
    pass


class Tool:
    name: str
    description: str

    def run(self, argument: str) -> str:
        raise NotImplementedError


@dataclass
class CalculatorTool(Tool):
    name: str = "calculator"
    description: str = "Evaluate safe arithmetic expressions."

    _ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
    }

    def _eval(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._ops:
            return self._ops[type(node.op)](self._eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in self._ops:
            return self._ops[type(node.op)](self._eval(node.left), self._eval(node.right))
        raise ToolError("Unsupported expression.")

    def run(self, argument: str) -> str:
        tree = ast.parse(argument, mode="eval")
        return str(self._eval(tree.body))


@dataclass
class TextSearchTool(Tool):
    corpus_dir: Path
    name: str = "text_search"
    description: str = "Search local text or markdown files for relevant lines."

    def run(self, argument: str) -> str:
        query = argument.lower().strip()
        if not query:
            raise ToolError("Query is empty.")
        hits = []
        for path in sorted(self.corpus_dir.glob("*")):
            if path.suffix.lower() not in {".txt", ".md"}:
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if query in line.lower():
                    hits.append(f"{path.name}: {line.strip()}")
        return "\n".join(hits[:10]) if hits else "No matching evidence found."


@dataclass
class CSVSummaryTool(Tool):
    name: str = "csv_summary"
    description: str = "Summarize a local CSV file."

    def run(self, argument: str) -> str:
        path = Path(argument.strip())
        if not path.exists() or path.suffix.lower() != ".csv":
            raise ToolError("Provide an existing CSV path.")
        df = pd.read_csv(path)
        return (
            f"rows={len(df)}, columns={len(df.columns)}, "
            f"column_names={list(df.columns)}, missing={int(df.isna().sum().sum())}"
        )
