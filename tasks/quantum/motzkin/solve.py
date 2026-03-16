"""Motzkin state — photonic experiment meta-program.

Best known: prefix_ok=-1, avg_fid=0.333 (fails at N=0).
Motzkin words use three symbols: 0='(' open, 1=')' close, 2='-' flat.
This is one of the hardest states to construct.

Edit this file to improve the ProgramSpec.
"""

from __future__ import annotations


def build_program() -> dict:
    """Return a ProgramSpec dict for the Motzkin state family.

    The program must generalize across system sizes N=0..4 where
    P(N) = 4 + 2*N vertices and K = 2 + N photon pairs.
    """
    return {
        "schema_version": "v1",
        "metadata": {"title": "motzkin", "notes": None},
        "edges": [
            {"u": "N+1", "v": "N+2", "cu": 0, "cv": 1, "w": 1},
            {"u": "N+2", "v": "2*N+3", "cu": 1, "cv": 0, "w": 1},
            {"u": "N+2", "v": "2*N+3", "cu": 2, "cv": 0, "w": 1},
        ],
        "loop": {
            "index": "ii",
            "range_expr": "N+1",
            "edges": [
                {"u": "ii", "v": "N+3+ii", "cu": 2, "cv": 0, "w": 1},
                {"u": "ii", "v": "ii+1", "cu": 0, "cv": 1, "w": 1},
                {"u": "ii+1", "v": "N+3+ii", "cu": 0, "cv": 0, "w": 1},
            ],
        },
    }
