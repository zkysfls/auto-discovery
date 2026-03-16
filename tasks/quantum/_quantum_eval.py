"""Shared evaluation bridge for quantum state discovery tasks.

Imports the metadesign_llm evaluation pipeline from the companion repo
and provides a uniform evaluate() helper for auto-discovery tasks.

Requires the llm-metadesign conda environment:
    conda run -n llm-metadesign python3 scripts/run_task.py quantum/<task>
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any

# Path to the metadesign_llm package
METADESIGN_REPO = Path("/home/zhengk5/llm-metadesign-quantum")

# N schedule and thresholds (mirror metadesign_llm defaults)
N_SCHEDULE = [0, 1, 2, 3, 4]
FIDELITY_THRESHOLD = 0.99


def _run_in_subprocess(program_json: dict, mode: str, timeout: int = 300) -> dict:
    """Evaluate a ProgramSpec in a subprocess to isolate pytheus imports.

    Returns the evaluation result dict from metadesign_llm.evaluator.
    """
    driver_code = f"""
import sys, json
sys.path.insert(0, {str(METADESIGN_REPO)!r})

from metadesign_llm.evaluator import evaluate_candidate, build_target_states

program = json.loads({json.dumps(json.dumps(program_json))})
mode = {mode!r}
n_schedule = {N_SCHEDULE!r}

targets = build_target_states(mode, n_schedule)
result = evaluate_candidate(program, targets, n_schedule=n_schedule)
print(json.dumps(result))
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(driver_code)
        driver_path = f.name

    try:
        proc = subprocess.run(
            [sys.executable, driver_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if proc.returncode != 0:
            return {
                "fidelities": {},
                "prefix_ok": -1,
                "avg_fid": 0.0,
                "error": f"Subprocess failed:\n{proc.stderr[-2000:]}",
                "success": False,
            }
        return json.loads(proc.stdout.strip())
    except subprocess.TimeoutExpired:
        return {
            "fidelities": {},
            "prefix_ok": -1,
            "avg_fid": 0.0,
            "error": f"Evaluation timed out after {timeout}s",
            "success": False,
        }
    except Exception as exc:
        return {
            "fidelities": {},
            "prefix_ok": -1,
            "avg_fid": 0.0,
            "error": str(exc),
            "success": False,
        }
    finally:
        Path(driver_path).unlink(missing_ok=True)


def evaluate_quantum_task(program_path: str, mode: str) -> dict[str, float]:
    """Load a solve module, call build_program(), and evaluate.

    This is the main entry point called by each task's evaluator.py.
    Returns a metrics dict compatible with auto-discovery's run_task.py.
    """
    # Dynamically load the solve module
    solve_path = Path(program_path).resolve()
    spec = importlib.util.spec_from_file_location("solve_module", solve_path)
    if spec is None or spec.loader is None:
        return _error_metrics(f"Cannot load module from {solve_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return _error_metrics(f"Import error:\n{traceback.format_exc()}")

    if not hasattr(module, "build_program"):
        return _error_metrics("solve.py must define build_program() -> dict")

    try:
        program = module.build_program()
    except Exception:
        return _error_metrics(f"build_program() raised:\n{traceback.format_exc()}")

    if not isinstance(program, dict):
        return _error_metrics(f"build_program() returned {type(program)}, expected dict")

    # Run evaluation in subprocess (isolates pytheus)
    result = _run_in_subprocess(program, mode)

    # Convert to auto-discovery metrics format
    fidelities = result.get("fidelities", {})
    prefix_ok = result.get("prefix_ok", -1)
    avg_fid = result.get("avg_fid", 0.0)
    success = result.get("success", False)
    error = result.get("error")

    # Primary metric: prefix_ok (how many consecutive N values pass)
    # normalized to [0, 1] as prefix_ok / len(N_SCHEDULE)
    n_total = len(N_SCHEDULE)
    score = (prefix_ok + 1) / n_total if prefix_ok >= 0 else 0.0

    metrics: dict[str, float] = {
        "score": score,
        "prefix_ok": float(prefix_ok),
        "avg_fid": avg_fid,
        "success": 1.0 if success else 0.0,
    }

    # Add per-N fidelities
    for n_val in N_SCHEDULE:
        key_str = str(n_val)
        metrics[f"fid_N{n_val}"] = fidelities.get(key_str, fidelities.get(n_val, 0.0))

    if error:
        metrics["error_msg"] = 0.0  # placeholder so it's numeric
        print(f"  evaluation note: {error}")

    return metrics


def _error_metrics(msg: str) -> dict[str, float]:
    """Return zero metrics with an error message printed."""
    print(f"  ERROR: {msg}")
    metrics: dict[str, float] = {
        "score": 0.0,
        "prefix_ok": -1.0,
        "avg_fid": 0.0,
        "success": 0.0,
    }
    for n_val in N_SCHEDULE:
        metrics[f"fid_N{n_val}"] = 0.0
    return metrics
