# Autonomous Task: quantum/motzkin

You are an autonomous research agent designing a photonic quantum experiment.

Your goal is to improve `tasks/quantum/motzkin/solve.py` so that its `build_program()` function returns a ProgramSpec that produces the Motzkin quantum state family with fidelity >= 0.99 for all system sizes N=0,1,2,3,4.

## Problem

Design a photonic experiment meta-program for the **Motzkin** quantum state family.

Motzkin words are sequences of three symbols: "(" (mode 0), ")" (mode 1), "-" (mode 2), where at every prefix opens >= closes. These generalize Dyck words by adding a "flat step". The number of Motzkin words of length n follows the Motzkin number sequence: 1, 1, 2, 4, 9, 21, 51, ...

### Target states (examples at N=0,1,2)

The evaluator tests N=0,1,2,3,4. The states below are provided as examples so you can understand the pattern. Your ProgramSpec must **generalize** — it is evaluated at N=3 (51 terms, 10 verts) and N=4 (127 terms, 12 verts) which are NOT shown here.

```
N=0 [4 verts, 4 terms]:  +1[axbyczdx]+1[axbzcydx]+1[azbxcydx]+1[azbzczdx]
N=1 [6 verts, 9 terms]:  +1[axbxcydyexfx]+1[axbycxdyexfx]+1[axbyczdzexfx]+1[axbzcydzexfx]+1[axbzczdyexfx]+1[azbxcydzexfx]+1[azbxczdyexfx]+1[azbzcxdyexfx]+1[azbzczdzexfx]
N=2 [8 verts, 21 terms]: +1[axbxcydyezfxgxhx]+1[axbxcydzeyfxgxhx]+1[axbxczdyeyfxgxhx]+1[axbycxdyezfxgxhx]+1[axbycxdzeyfxgxhx]+1[axbyczdxeyfxgxhx]+1[axbyczdzezfxgxhx]+1[axbzcxdyeyfxgxhx]+1[axbzcydxeyfxgxhx]+1[axbzcydzezfxgxhx]+1[axbzczdyezfxgxhx]+1[axbzczdzeyfxgxhx]+1[azbxcxdyeyfxgxhx]+1[azbxcydxeyfxgxhx]+1[azbxcydzezfxgxhx]+1[azbxczdyezfxgxhx]+1[azbxczdzeyfxgxhx]+1[azbzcxdyezfxgxhx]+1[azbzcxdzeyfxgxhx]+1[azbzczdxeyfxgxhx]+1[azbzczdzezfxgxhx]
```

### Current best

prefix_ok=-1 (fails at N=0). avg_fid=0.333. This is one of the hardest states.

## ProgramSpec format

```json
{
  "schema_version": "v1",
  "metadata": {"title": "...", "notes": null},
  "edges": [{"u": "<expr>", "v": "<expr>", "cu": 0, "cv": 0, "w": 1}],
  "loop": {"index": "ii", "range_expr": "<expr>", "edges": [...]}
}
```

- `u`, `v`: vertex indices (expressions over N, and ii in loop)
- `cu`, `cv`: mode/color 0, 1, or 2
- `w`: +1 or -1
- P(N) = 4 + 2*N vertices, K = 2 + N photon pairs

### Notation
- Vertices: a=0, b=1, c=2, ...; Modes: x=0 ("("), y=1 (")"), z=2 ("-")

### Critical constraint: Uniform Perfect Matching
ALL matchings must have exactly K = 2+N edges covering all P(N) vertices.

## Run command

```bash
conda run -n llm-metadesign python3 scripts/run_task.py quantum/motzkin --notes "<short experiment note>"
```

## Files

Read: `tasks/quantum/motzkin/task.json`, `evaluator.py`, `program.md`, `tasks/quantum/_quantum_eval.py`

Modify: `tasks/quantum/motzkin/solve.py` only.

## Experiment tactics

### Understanding Motzkin structure
- Three modes used: 0 (open), 1 (close), 2 (flat/dash)
- All terms have equal weight (+1)
- Term counts: N=0: 4, N=1: 9, N=2: 21 (Motzkin numbers for length 3+N)
- More terms than Dyck because the flat step adds combinatorial possibilities
- The current program completely fails at N=0 — start by getting N=0 right

### Analyzing N=0 target
At N=0 (4 vertices, K=2), the 4 terms are:
- `axbyczdx` → vertices 0,1,2,3 in modes 0,1,2,0 → word "(-)(" — wait, that's not valid
- Actually: vertex modes map to Motzkin symbols, and the valid Motzkin words of length ii=3 give these 4 kets
- Terms: ()(, ()z, z(), zzz — i.e., the 4 Motzkin words of length 3

### Promising directions
- Start from scratch: the current program barely works
- Build a graph that naturally generates Motzkin-number matchings
- Motzkin words have recursive structure: M(n) = M(n-1) + sum_{k=0}^{n-2} M(k)*M(n-2-k)
- This recursion combines "flat step" (first term) with "matched pair" (second term)
- Study the simpler Dyck task first — Motzkin adds one extra symbol
- Consider complete bipartite subgraphs or layered structures

### Keep / discard rule
Keep only if `score` strictly improves. Revert and try another approach if not.
