# Autonomous Task: quantum/majumdar_ghosh

You are an autonomous research agent designing a photonic quantum experiment.

Your goal is to improve `tasks/quantum/majumdar_ghosh/solve.py` so that its `build_program()` function returns a ProgramSpec that produces the Majumdar-Ghosh quantum state family with fidelity >= 0.99 for all system sizes N=0,1,2,3,4.

## Problem

Design a photonic experiment meta-program for the **Majumdar-Ghosh** quantum state.

The Majumdar-Ghosh state is the exact ground state of the J1-J2 Heisenberg spin chain at J2/J1 = 0.5 with periodic boundary conditions. It uses 3x3 transfer matrices:
- A[1] = [[0,1,0],[0,0,-1],[0,0,0]]
- A[0] = [[0,0,0],[1,0,0],[0,1,0]]

Weights are Tr(A[s1]*A[s2]*...*A[sL]) where L = P(N) = 4+2N.

### Target states (examples at N=0,1,2)

The evaluator tests N=0,1,2,3,4. The states below are provided as examples so you can understand the pattern. Your ProgramSpec must **generalize** — it is evaluated at N=3 (60 terms, 10 verts) and N=4 (126 terms, 12 verts) which are NOT shown here.

```
N=0 [4 verts, 6 terms]:  -1[axbxcydy]+2[axbycxdy]-1[axbycydx]-1[aybxcxdy]+2[aybxcydx]-1[aybycxdx]
N=1 [6 verts, 12 terms]: -1[axbxcydxeyfy]+1[axbxcydyexfy]+1[axbycxdxeyfy]-1[axbycxdyeyfx]-1[axbycydxexfy]+1[axbycydxeyfx]-1[aybxcxdyexfy]+1[aybxcxdyeyfx]+1[aybxcydxexfy]-1[aybxcydyexfx]-1[aybycxdxeyfx]+1[aybycxdyexfx]
N=2 [8 verts, 30 terms]: (weights are -1, +1, or +2; too long to display)
```

### Current best

prefix_ok=-1 (fails at N=0). However, this state was previously solved in an earlier run (2026-03-01) but the solution was lost. It should be recoverable.

## ProgramSpec format

```json
{
  "schema_version": "v1",
  "metadata": {"title": "...", "notes": null},
  "edges": [{"u": "<expr>", "v": "<expr>", "cu": 0, "cv": 0, "w": 1}],
  "loop": {"index": "ii", "range_expr": "<expr>", "edges": [...]}
}
```

- `u`, `v`: vertex index expressions
- `cu`, `cv`: mode 0 or 1 (this state only uses 2 modes)
- `w`: +1 or -1
- P(N) = 4 + 2*N vertices, K = 2 + N photon pairs

### Critical constraint: Uniform Perfect Matching
ALL matchings must have exactly K = 2+N edges.

## Run command

```bash
conda run -n llm-metadesign python3 scripts/run_task.py quantum/majumdar_ghosh --notes "<short experiment note>"
```

## Files

Read: `tasks/quantum/majumdar_ghosh/task.json`, `evaluator.py`, `program.md`, `tasks/quantum/_quantum_eval.py`

Modify: `tasks/quantum/majumdar_ghosh/solve.py` only.

## Experiment tactics

### Understanding Majumdar-Ghosh structure
- Uses only 2 modes: x=0 and y=1 (spin up/down)
- Weights come from traces of 3x3 matrix products — can be -1, +1, or +2
- Periodic boundary conditions (trace operation) mean the last vertex connects back to the first
- At N=0: 6 terms with weights -1, +2, -1, -1, +2, -1
- At N=1: 12 terms with weights alternating +1/-1
- The weight +2 appears at specific configurations (trace of identity-like products)

### Key observations
- The current program uses wrap-around edges (vertex `3+2*N` to vertex `0`) — this captures periodicity
- The loop runs over `3+2*N` iterations with nearest-neighbor coupling
- But it completely fails — the edge structure may be too simple

### Promising directions
- The state was solved before, suggesting it IS possible with the right edge configuration
- The MPS structure with 3x3 matrices means the graph needs to encode the transfer matrix
- Consider next-nearest-neighbor edges (not just ii to ii+1)
- The weights +2 suggest some edges need to "double up" via coalescing
- Try connecting each vertex to both its neighbor and its next-next neighbor
- Consider a singlet-pair-covering structure: (0,1), (2,3), ... with alternating phases

### Keep / discard rule
Keep only if `score` strictly improves. Revert and try another approach if not.
