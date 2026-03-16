"""GHZ3D/GHZ3D state — photonic experiment meta-program.

Best known: prefix_ok=0, avg_fid=1.0 (passes N=0 only, fails at N=1).
This is a tensor product of two 3-dimensional GHZ states, each using
3 modes (x=0, y=1, z=2). The state has 9 terms at each N.

Edit this file to improve the ProgramSpec.
"""

from __future__ import annotations


def build_program() -> dict:
    """Return a ProgramSpec dict for the GHZ3D/GHZ3D state family.

    The program must generalize across system sizes N=0..4 where
    P(N) = 4 + 2*N vertices and K = 2 + N photon pairs.
    """
    return {
        "schema_version": "v1",
        "metadata": {"title": "ghz3d_ghz3d", "notes": None},
        "edges": [
            {"u": "0", "v": "1", "cu": 0, "cv": 0, "w": 1},
            {"u": "0", "v": "1", "cu": 1, "cv": 1, "w": 1},
            {"u": "0", "v": "1", "cu": 2, "cv": 2, "w": 1},
            {"u": "2+N", "v": "3+N", "cu": 0, "cv": 0, "w": 1},
            {"u": "2+N", "v": "3+N", "cu": 1, "cv": 1, "w": 1},
            {"u": "2+N", "v": "3+N", "cu": 2, "cv": 2, "w": 1},
        ],
        "loop": {
            "index": "ii",
            "range_expr": "N",
            "edges": [
                {"u": "2+ii", "v": "3+ii", "cu": 0, "cv": 0, "w": 1},
                {"u": "2+ii", "v": "3+ii", "cu": 1, "cv": 1, "w": 1},
                {"u": "2+ii", "v": "3+ii", "cu": 2, "cv": 2, "w": 1},
                {"u": "4+N+ii", "v": "5+N+ii", "cu": 0, "cv": 0, "w": 1},
                {"u": "4+N+ii", "v": "5+N+ii", "cu": 1, "cv": 1, "w": 1},
                {"u": "4+N+ii", "v": "5+N+ii", "cu": 2, "cv": 2, "w": 1},
            ],
        },
    }
