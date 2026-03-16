"""Majumdar-Ghosh state — photonic experiment meta-program.

Best known: prefix_ok=-1, avg_fid=0.0 (fails at N=0).
The Majumdar-Ghosh state is the ground state of the J1-J2 Heisenberg chain
at J2/J1 = 0.5. It has weighted terms defined by traces of matrix products
of 3x3 transfer matrices A[0], A[1].

Note: this state was previously solved in an earlier run (2026-03-01) but
the solution was not preserved. It should be recoverable.

Edit this file to improve the ProgramSpec.
"""

from __future__ import annotations


def build_program() -> dict:
    """Return a ProgramSpec dict for the Majumdar-Ghosh state family.

    The program must generalize across system sizes N=0..4 where
    P(N) = 4 + 2*N vertices and K = 2 + N photon pairs.
    """
    return {
        "schema_version": "v1",
        "metadata": {"title": "majumdar_ghosh", "notes": None},
        "edges": [
            {"u": "3+2*N", "v": "0", "cu": 0, "cv": 1, "w": 1},
            {"u": "3+2*N", "v": "0", "cu": 1, "cv": 0, "w": -1},
        ],
        "loop": {
            "index": "ii",
            "range_expr": "3+2*N",
            "edges": [
                {"u": "ii", "v": "ii+1", "cu": 0, "cv": 1, "w": 1},
                {"u": "ii", "v": "ii+1", "cu": 1, "cv": 0, "w": -1},
            ],
        },
    }
