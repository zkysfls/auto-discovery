"""AKLT state — photonic experiment meta-program.

Best known: prefix_ok=0, avg_fid=1.0 (passes N=0 only, fails at N=1).
The AKLT state is a spin-1 valence-bond-solid ground state defined by
matrix product operators A[0], A[1], A[2] with trace-based weights.

Edit this file to improve the ProgramSpec.
"""

from __future__ import annotations


def build_program() -> dict:
    """Return a ProgramSpec dict for the AKLT state family.

    The program must generalize across system sizes N=0..4 where
    P(N) = 4 + 2*N vertices and K = 2 + N photon pairs.
    """
    return {
        "schema_version": "v1",
        "metadata": {"title": "aklt", "notes": None},
        "edges": [
            {"u": "N+2", "v": "2*N+3", "cu": 0, "cv": 0, "w": 1},
            {"u": "2", "v": "N+3", "cu": 0, "cv": 0, "w": -1},
            {"u": "0", "v": "N+3", "cu": 0, "cv": 0, "w": 1},
            {"u": "N", "v": "3", "cu": 0, "cv": 0, "w": -1},
            {"u": "N", "v": "2*N+3", "cu": 2, "cv": 0, "w": 1},
            {"u": "0", "v": "3", "cu": 2, "cv": 0, "w": -1},
        ],
        "loop": {
            "index": "ii",
            "range_expr": "N+1",
            "edges": [
                {"u": "ii", "v": "ii+1", "cu": 2, "cv": 0, "w": -1},
                {"u": "N+2+ii", "v": "N+3+ii", "cu": 0, "cv": 0, "w": 1},
                {"u": "ii", "v": "N+2+ii", "cu": 0, "cv": 0, "w": 1},
                {"u": "ii", "v": "N+3+ii", "cu": 1, "cv": 0, "w": 1},
                {"u": "ii+1", "v": "N+2+ii", "cu": 1, "cv": 0, "w": 1},
                {"u": "ii+1", "v": "N+3+ii", "cu": 2, "cv": 0, "w": -1},
            ],
        },
    }
