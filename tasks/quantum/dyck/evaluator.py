"""Dyck state evaluator — delegates to shared quantum evaluation bridge."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _quantum_eval import evaluate_quantum_task


def evaluate(program_path: str) -> dict:
    return evaluate_quantum_task(program_path, mode="dyck")
