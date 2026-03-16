"""Dyck state — photonic experiment meta-program.

Best known: prefix_ok=1, avg_fid=1.0 (passes N=0,1; fails at N=2).
Dyck words are balanced parenthesizations counted by Catalan numbers.
The state uses modes 1 (open) and 2 (close) as Dyck symbols.

Edit this file to improve the ProgramSpec.
"""

from __future__ import annotations


def build_program() -> dict:
    """Return a ProgramSpec dict for the Dyck state family.

    The program must generalize across system sizes N=0..4 where
    P(N) = 4 + 2*N vertices and K = 2 + N photon pairs.
    """
    return {
        "schema_version": "v1",
        "metadata": {"title": "dyck", "notes": None},
        "edges": [],
        "loop": {
            "index": "ii",
            "range_expr": "N+1",
            "edges": [
                {"u": "0", "v": "2*ii+1", "cu": 1, "cv": 2, "w": 1},
                {"u": "0", "v": "2*ii+2", "cu": 1, "cv": 2, "w": 1},
                {"u": "2*ii+1", "v": "2*ii+2", "cu": 1, "cv": 2, "w": 1},
                {"u": "2*ii+2", "v": "2*ii+3", "cu": 1, "cv": 2, "w": 1},
                {"u": "ii+1", "v": "2*N+3", "cu": 1, "cv": 2, "w": 1},
            ],
        },
    }
