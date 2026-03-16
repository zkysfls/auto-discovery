# Autonomous Task: quantum/dyck

You are an autonomous research agent designing a photonic quantum experiment.

Your goal is to improve `tasks/quantum/dyck/solve.py` so that its `build_program()` function returns a ProgramSpec that produces the Dyck quantum state family with fidelity >= 0.99 for all system sizes N=0,1,2,3,4.

## Problem

Design a photonic experiment meta-program for the **Dyck** quantum state family.

Dyck words are balanced parenthesizations: sequences of "(" (mode 1) and ")" (mode 2) where at every prefix the number of opens >= closes. The number of Dyck words of length 2n is the Catalan number C_n.

The quantum state is an equal superposition of all Dyck words of length P(N)/2 = 2+N, padded to P(N) vertices.

### Target states (examples at N=0,1,2)

The evaluator tests N=0,1,2,3,4. The states below are provided as examples so you can understand the pattern. Your ProgramSpec must **generalize** — it is evaluated at N=3 (42 terms, 10 verts) and N=4 (132 terms, 12 verts) which are NOT shown here.

```
N=0 [4 verts, 2 terms]:  +1[aybyczdz]+1[aybzcydz]
N=1 [6 verts, 5 terms]:  +1[aybycydzezfz]+1[aybyczdyezfz]+1[aybyczdzeyfz]+1[aybzcydyezfz]+1[aybzcydzeyfz]
N=2 [8 verts, 14 terms]: +1[aybycydyezfzgzhz]+1[aybycydzeyfzgzhz]+1[aybycydzezfygzhz]+1[aybycydzezfzgyhz]+1[aybyczdyeyfzgzhz]+1[aybyczdyezfygzhz]+1[aybyczdyezfzgyhz]+1[aybyczdzeyfygzhz]+1[aybyczdzeyfzgyhz]+1[aybzcydyeyfzgzhz]+1[aybzcydyezfygzhz]+1[aybzcydyezfzgyhz]+1[aybzcydzeyfygzhz]+1[aybzcydzeyfzgyhz]
```

### Current best

prefix_ok=1 (passes N=0 and N=1, fails at N=2). avg_fid=1.0 for passing values.

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
- `u`, `v`: vertex indices as string expressions over N (base edges) or N and ii (loop edges)
- `cu`, `cv`: color/mode indices (0, 1, or 2)
- `w`: weight (+1 or -1)

### Scaling
- P(N) = 4 + 2*N vertices total
- K = 2 + N photon pairs
- Vertices: a=0, b=1, c=2, d=3, e=4, f=5, ...
- Modes: x=0, y=1 (open paren), z=2 (close paren)

### Critical constraint: Uniform Perfect Matching
Each detection event uses exactly K = 2+N edges. ALL perfect matchings must have size K.

## Run command

```bash
conda run -n llm-metadesign python3 scripts/run_task.py quantum/dyck --notes "<short experiment note>"
```

## Files

Read: `tasks/quantum/dyck/task.json`, `evaluator.py`, `program.md`, `tasks/quantum/_quantum_eval.py`

Modify: `tasks/quantum/dyck/solve.py` only.

## Experiment tactics

### Understanding Dyck structure
- All terms have equal weight (+1), no negative or weighted terms
- Mode pattern: vertex 0 always mode 1 (open), last vertices tend to mode 2 (close)
- The number of terms follows Catalan numbers: C_2=2, C_3=5, C_4=14, C_5=42, C_6=132
- The current program passes N=0 (2 terms) and N=1 (5 terms) but fails N=2 (14 terms)
- At N=2 with 8 vertices and K=4 edges, the graph needs 14 perfect matchings

### Promising directions
- Analyze which graph topologies naturally produce Catalan-number matchings
- The recursive structure of Dyck words (a Dyck word is either empty, or "(w1)w2" where w1,w2 are Dyck words) might map to a recursive graph construction
- Study which edges the current program generates at N=2 and compare to required matchings
- Try path-like or tree-like graph structures
- Consider that modes 1 and 2 act as "open" and "close" brackets

### Keep / discard rule
Keep only if `score` strictly improves. Revert and try another approach if not.
