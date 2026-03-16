# Autonomous Task: quantum/aklt

You are an autonomous research agent designing a photonic quantum experiment.

Your goal is to improve `tasks/quantum/aklt/solve.py` so that its `build_program()` function returns a ProgramSpec that produces the AKLT quantum state family with fidelity >= 0.99 for all system sizes N=0,1,2,3,4.

## Problem

Design a photonic experiment meta-program (a JSON "ProgramSpec") that encodes a generalizable construction rule for the **AKLT** (Affleck-Kennedy-Lieb-Tasaki) quantum state.

The AKLT state is a spin-1 valence-bond-solid ground state. It is defined via matrix product operators:
- A[0] = [[0, 1/sqrt(2)], [0, 0]]
- A[1] = [[-1/2, 0], [0, 1/2]]
- A[2] = [[0, 0], [-1/sqrt(2), 0]]

State terms have weights = Tr(A[s1] * A[s2] * ... * A[sL]) * 2^(L-1), where L = ii - 1 = 2 + N.

### Target states (examples at N=0,1,2)

The evaluator tests N=0,1,2,3,4. The states below are provided as examples so you can understand the pattern. Your ProgramSpec must **generalize** — it is evaluated at N=3 (30 terms, 10 verts) and N=4 (63 terms, 12 verts) which are NOT shown here.

```
N=0 [4 verts, 3 terms]:  -1[axbzcxdx]+1[aybycxdx]-1[azbxcxdx]
N=1 [6 verts, 6 terms]:  -1[axbyczdxexfx]+1[axbzcydxexfx]+1[aybxczdxexfx]-1[aybzcxdxexfx]-1[azbxcydxexfx]+1[azbycxdxexfx]
N=2 [8 verts, 15 terms]: -1[axbycydzexfxgxhx]+1[axbyczdyexfxgxhx]+2[axbzcxdzexfxgxhx]-1[axbzcydyexfxgxhx]+1[aybxcydzexfxgxhx]-1[aybxczdyexfxgxhx]-1[aybycxdzexfxgxhx]+1[aybycydyexfxgxhx]-1[aybyczdxexfxgxhx]-1[aybzcxdyexfxgxhx]+1[aybzcydxexfxgxhx]-1[azbxcydyexfxgxhx]+2[azbxczdxexfxgxhx]+1[azbycxdyexfxgxhx]-1[azbycydxexfxgxhx]
```

### Current best

prefix_ok=0 (passes N=0 only, fails at N=1). avg_fid=1.0 at N=0.

## ProgramSpec format

A ProgramSpec encodes a photonic experiment as a graph with parametric edges:

```json
{
  "schema_version": "v1",
  "metadata": {"title": "...", "notes": null},
  "edges": [
    {"u": "<expr>", "v": "<expr>", "cu": 0, "cv": 0, "w": 1}
  ],
  "loop": {
    "index": "ii",
    "range_expr": "<expr over N>",
    "edges": [
      {"u": "<expr>", "v": "<expr>", "cu": 0, "cv": 0, "w": 1}
    ]
  }
}
```

### Edge fields
- `u`, `v`: vertex indices as string expressions over N (base edges) or N and ii (loop edges). Allowed operators: +, -, *. No division, no powers, no functions.
- `cu`, `cv`: color/mode indices (0, 1, or 2)
- `w`: weight (+1 or -1)

### Scaling
- P(N) = 4 + 2*N vertices total
- K = 2 + N photon pairs (edges in each perfect matching)
- N=0: 4 vertices (a,b,c,d), K=2
- N=1: 6 vertices, K=3
- N=2: 8 vertices, K=4
- N=3: 10 vertices, K=5
- N=4: 12 vertices, K=6

### State string notation
- `+w[aXbYcZ...]` means coefficient w; vertex a in mode X, vertex b in mode Y, ...
- Vertices: a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, ...
- Modes: x=0 (horizontal), y=1 (vertical), z=2

### Critical constraint: Uniform Perfect Matching
Each detection event uses exactly K = 2+N edges. The graph must ONLY allow perfect matchings of size K. Graphs with mixed matching sizes crash with "inhomogeneous shape" error.

Practical rule: design the graph so exactly K edges cover all P(N) vertices as K disjoint pairs — no vertex left uncovered, no vertex used twice.

## Setup

Before doing experiments:

1. Confirm the current branch and directory
2. Read the relevant files listed below
3. Run the baseline once before making changes

## Files

Read:
- `tasks/quantum/aklt/task.json`
- `tasks/quantum/aklt/evaluator.py`
- `tasks/quantum/aklt/program.md`
- `tasks/quantum/_quantum_eval.py`

Modify:
- `tasks/quantum/aklt/solve.py`

Do not edit any other file.

## Run command

After each change, run:

```bash
conda run -n llm-metadesign python3 scripts/run_task.py quantum/aklt --notes "<short experiment note>"
```

Important printed fields:
- `score` — primary metric (0 to 1, proportion of N values passing)
- `prefix_ok` — how many consecutive N values pass (target: 4)
- `avg_fid` — average fidelity across tested N values
- `fid_N0` through `fid_N4` — per-N fidelities

## Ground truth

- `evaluator.py` is the ground truth. Judge changes only by verified evaluator output.
- Do not change the evaluator, runner, or task metadata.

## Mutation policy

- Only edit `solve.py`
- The `build_program()` function must return a valid ProgramSpec dict
- Keep the solution self-contained

### What you can change in solve.py
- The edge list (base edges and loop edges)
- The loop range expression
- Add helper functions that compute edges algorithmically
- Try completely different graph topologies
- Use Python logic to construct the ProgramSpec programmatically

### What counts as improvement
- Higher `prefix_ok` (more consecutive N values passing)
- Higher `avg_fid` if prefix_ok is tied
- Target: `success=1.0` (all N=0..4 pass with fidelity >= 0.99)

## Keep / discard rule

Keep a change only if:
- The evaluator runs successfully
- The new `score` is strictly better than the current baseline

If worse, revert `solve.py` and try another idea.

## Experiment tactics

### Understanding the AKLT structure
- AKLT uses 3 modes (spin-1): mode 0, 1, 2
- Weights come from traces of matrix products — they can be +1, -1, or +2
- The state has periodic boundary conditions (trace operation)
- At N=0: 3 terms with weights -1, +1, -1
- At N=1: 6 terms with weights alternating +1/-1
- At N=2: 15 terms with weights -1, +1, +2, -1, ...

### Promising directions
- Study how the target state terms relate to graph matchings
- The current program passes N=0 but fails N=1 — analyze what changes at N=1
- Look at the vertex connectivity pattern: which vertices must be connected?
- Consider that modes 0,1,2 all appear on the first few vertices but only mode 0 on the later ones
- Try different loop structures that better capture the MPS transfer matrix pattern
- The periodic boundary condition (trace) may require wrap-around edges

### Less promising
- Random edge modifications without understanding the structure
- Adding complexity without testing intermediate steps
