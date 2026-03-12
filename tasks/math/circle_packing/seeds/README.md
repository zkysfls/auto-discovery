# circle_packing seeds

This directory stores a small portfolio of verified `circle_packing` seeds.

## Purpose

`autoresearch`-style runs often advance one incumbent branch. That works well when improvements compose cleanly.

For geometric discovery tasks, good ideas are often not linearly composable. Different layouts can represent different construction families, and a slightly weaker seed may still be the best launch point for a later improvement.

So this task keeps:

- one mutable working file: `solve.py`
- a small read-only archive of seed snapshots: `seeds/*.py`

## Files

- `seed_index.tsv`: machine-readable seed metadata
- `*.py`: self-contained seed snapshots with the same `run_packing()` API as `solve.py`

## Seed promotion rule

Promote a candidate to a seed when it is at least one of:

- the current best verified score
- a clearly different construction family
- a useful parent for future local search or hybridization

Do not promote every tiny variant. The archive should stay small and interpretable.

## Seed ids

Use short stable ids such as:

- `cp-baseline-ring`
- `cp-boundary-ladder-v1`
- `cp-asym-shell-polish-v2`

## Workflow

1. read `seed_index.tsv`
2. inspect one or two relevant seed snapshots
3. copy one seed into `solve.py` manually if you want to launch from it
4. run experiments only by editing `solve.py`
5. promote a new seed later if the run discovers something meaningfully new
