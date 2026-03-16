# Autonomous Task: quantum/ghz3d_ghz3d

You are an autonomous research agent designing a photonic quantum experiment.

Your goal is to improve `tasks/quantum/ghz3d_ghz3d/solve.py` so that its `build_program()` function returns a ProgramSpec that produces the GHZ3D/GHZ3D quantum state family with fidelity >= 0.99 for all system sizes N=0,1,2,3,4.

## Problem

Design a photonic experiment meta-program for the **GHZ3D/GHZ3D** quantum state.

This is a tensor product of two 3-dimensional GHZ states. Each "half" of the system (first P(N)/2 and last P(N)/2 vertices) independently forms a 3-mode GHZ state. The combined state has 3x3 = 9 terms at every N.

### Target states (examples at N=0,1,2)

The evaluator tests N=0,1,2,3,4. The states below are provided as examples so you can understand the pattern. Your ProgramSpec must **generalize** — it is evaluated at N=3 (9 terms, 10 verts) and N=4 (9 terms, 12 verts) which are NOT shown here. Note: GHZ3D/GHZ3D always has exactly 9 terms regardless of N.

```
N=0 [4 verts, 9 terms]: +1[axbxcxdx]+1[axbxcydy]+1[axbxczdz]+1[aybycxdx]+1[aybycydy]+1[aybyczdz]+1[azbzcxdx]+1[azbzcydy]+1[azbzczdz]
N=1 [6 verts, 9 terms]: +1[axbxcxdxexfx]+1[axbxcxdyeyfy]+1[axbxcxdzezfz]+1[aybycydxexfx]+1[aybycydyeyfy]+1[aybycydzezfz]+1[azbzczdxexfx]+1[azbzczdyeyfy]+1[azbzczdzezfz]
N=2 [8 verts, 9 terms]: +1[axbxcxdxexfxgxhx]+1[axbxcxdxeyfygyhy]+1[axbxcxdxezfzgzhz]+1[aybycydyexfxgxhx]+1[aybycydyeyfygyhy]+1[aybycydyezfzgzhz]+1[azbzczdzexfxgxhx]+1[azbzczdzeyfygyhy]+1[azbzczdzezfzgzhz]
```

### Current best

prefix_ok=0 (passes N=0 only, fails at N=1). avg_fid=1.0 at N=0.

## ProgramSpec format

```json
{
  "schema_version": "v1",
  "metadata": {"title": "...", "notes": null},
  "edges": [{"u": "<expr>", "v": "<expr>", "cu": 0, "cv": 0, "w": 1}],
  "loop": {"index": "ii", "range_expr": "<expr>", "edges": [...]}
}
```

- `u`, `v`: vertex index expressions (N for base, N and ii for loop)
- `cu`, `cv`: mode 0, 1, or 2
- `w`: +1 or -1
- P(N) = 4 + 2*N vertices, K = 2 + N photon pairs
- Modes: x=0, y=1, z=2

### Critical constraint: Uniform Perfect Matching
ALL matchings must have exactly K = 2+N edges. No mixed matching sizes.

## Run command

```bash
conda run -n llm-metadesign python3 scripts/run_task.py quantum/ghz3d_ghz3d --notes "<short experiment note>"
```

## Files

Read: `tasks/quantum/ghz3d_ghz3d/task.json`, `evaluator.py`, `program.md`, `tasks/quantum/_quantum_eval.py`

Modify: `tasks/quantum/ghz3d_ghz3d/solve.py` only.

## Experiment tactics

### Understanding GHZ3D/GHZ3D structure
- The state is separable: first_half tensor second_half
- First half: vertices 0..P(N)/2-1, all same mode (GHZ3D = equal superposition of all-0, all-1, all-2)
- Second half: vertices P(N)/2..P(N)-1, same structure
- 9 terms = 3 choices for first half mode × 3 choices for second half mode
- All weights are +1

### Key insight: two independent GHZ blocks
- The 2D GHZ (modes 0,1) was solved: pair vertices (2i, 2i+1) with edges in modes 0-0 and 1-1
- GHZ3D adds mode 2-2 edges to each pair
- The challenge is splitting P(N) vertices into two groups that each form independent GHZ3D
- At N=0: vertices {0,1} form block 1, {2,3} form block 2 — 2 pairs, each with 3 mode edges
- At N=1: vertices {0,1,2} form block 1 (3 verts), {3,4,5} form block 2 — but 3 is odd!
- This is the core problem: with odd vertices per block, you can't pair them all

### The pairing challenge at N=1
- P(1) = 6 vertices, K=3 pairs. First half = vertices 0,1,2 (3 vertices, can't pair evenly)
- The GHZ structure requires all vertices in a block to share the same mode
- But K=3 means 3 pairs total, and you need pairs that couple within each block
- Possible: 1 cross-block pair + structured intra-block edges?
- Or: different vertex partition than 50/50 split

### Promising directions
- Study the working GHZ/GHZ solution (2-mode version) for insight — it may have a similar cross-block structure
- Consider that the "split" might not be at P(N)/2 but follow a different pattern
- Try chain-like coupling: pair (0,1), (2,3), (4,5) with appropriate mode structure
- The key constraint is that all matchings must select exactly one mode per pair

### Keep / discard rule
Keep only if `score` strictly improves. Revert and try another approach if not.
