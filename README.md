# auto-discovery

`auto-discovery` starts from a simple question:

if we want Codex to act like a discovery agent on math optimization tasks, do we really need a large framework like SkyDiscover, or can a much smaller scaffold already get us most of the useful behavior?

This repo is my attempt to answer that question in the smallest practical way.

The two closest references behind this thought are:

- [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch)
- [`skydiscover-ai/skydiscover`](https://github.com/skydiscover-ai/skydiscover)

The core bet is:

- a strong task-local `program.md`
- one mutable solution file
- a fixed evaluator
- tracked milestone results
- and `git worktree` for parallel runs

may already be enough to make Codex iterate usefully on benchmark tasks, without first building a heavy discovery framework.

So this repo is intentionally small. It is not trying to reimplement the full SkyDiscover search stack or a full agent framework. It is a hackable middle ground: import useful benchmarks, keep evaluators fixed, and let Codex iterate directly against `program.md` plus one mutable task file.

The benchmark source of truth can stay in `references/`, but the runnable tasks in this repo are self-contained. `references/` is ignored by git on purpose.

Evaluators and several task scaffolds in `tasks/math/` are adapted from the SkyDiscover benchmark definitions, then repackaged into self-contained task directories for this repo.

## Current focus

The current scope is intentionally narrow:

- imported math optimization tasks, mostly from SkyDiscover
- fixed evaluator plus one mutable `solve.py` per task
- task-local `program.md` as the main Codex instruction surface
- git worktrees for parallel runs when needed

That makes the repo easy to fork, easy to inspect, and easy to run with a bare Codex session.

## Validating the results

The promoted `auto-discovery` values recorded in each task's `results.tsv` are meant to be reproducible from the checked-in task files on `main`.

To validate a result locally, run the fixed evaluator for the corresponding task:

```bash
python scripts/run_task.py math/circle_packing
python scripts/run_task.py math/circle_packing_rect
python scripts/run_task.py math/heilbronn_triangle
python scripts/run_task.py math/minimizing_max_min_dist/2
python scripts/run_task.py math/minimizing_max_min_dist/3
```

What to compare:

- `circle_packing`: compare `sum_radii`
- `circle_packing_rect`: compare `radii_sum`
- `heilbronn_triangle`: compare `min_area_normalized`
- `minimizing_max_min_dist/2`: compare `inverse_min_max_ratio`
- `minimizing_max_min_dist/3`: compare `inverse_min_max_ratio`

The exact milestone history for each promoted result is tracked in that task's `results.tsv`. If a value in `main` changes, rerun the corresponding command and update the task-local milestone record.

## Selected comparisons

I still keep a small comparison table here because it is the clearest evidence for the core question behind this repo: can a very small scaffold still get competitive results on some math optimization tasks?

- For `circle_packing`, `circle_packing_rect`, and `heilbronn_triangle`, higher is better.
- For `minimizing_max_min_dist/2` and `minimizing_max_min_dist/3`, the table uses the inverse metric `(d_max / d_min)^2`, so lower is better.
- `-` means the published source I checked does not report that exact task/result pair.
- Bold marks the numerically best shown value in that column. Rounded published values can hide ties or tiny gaps.

| Method | Circle Packing Square `n=26` `↑` | Circle Packing Rectangle `n=21` `↑` | Heilbronn Triangle `n=11` `↑` | Inverse Max/Min Dist `n=16,d=2` `↓` | Inverse Max/Min Dist `n=14,d=3` `↓` |
| --- | --- | --- | --- | --- | --- |
| AlphaEvolve | `2.6358627564136983` | `2.3658321334167627` | **`0.036529889880030156`** | `12.88926611203463` | `4.165849767` |
| SkyDiscover (best published AdaEvolve/EvoX) | `2.63598308` | `2.36583237` | `0.036` | `-` | `4.16579879192` |
| LoongFlow | `2.6359829624734026` | `2.365832229500823` | `0.0365298898793351` | `12.889243547212832` | `-` |
| auto-discovery | **`2.63598308911`** | **`2.36584169299`** | **`0.036529889880030156`** | **`12.8892299077`** | **`4.16578347458007`** |

These are reference points, not a perfectly controlled apples-to-apples benchmark. The external systems use different backbones and reporting conventions, and some published tables round values aggressively.

## Layout

```text
tasks/
  math/
    circle_packing/
      task.json
      program.md
      evaluator.py
      solve.py
      seeds/
        seed_index.tsv
scripts/
  _tasks.py
  list_tasks.py
  run_task.py
  spawn_agents.py
references/
docs/
```

## Quick start

```bash
python scripts/list_tasks.py
python scripts/run_task.py math/circle_packing --notes baseline
python scripts/spawn_agents.py math/circle_packing
```

`spawn_agents.py` creates one git worktree per task and prints the Codex prompt to use in that worktree.

`python scripts/run_task.py ...` appends raw local evaluations to `run_history.tsv`. Each task's tracked `results.tsv` is reserved for curated milestones that you want visible on GitHub, and can use task-specific human-friendly columns such as both normalized score and raw objective value.

## Task contract

Each task directory contains:

- `task.json`: machine-readable task metadata
- `program.md`: Codex instructions for the task
- `evaluator.py`: fixed evaluator exposing `evaluate(program_path)`
- `solve.py`: the file Codex is expected to improve

Tasks may also keep a small read-only seed archive under `seeds/`. This supports multiple construction families across runs without letting one run edit the whole archive.

The framework uses JSON instead of YAML for task metadata so the runner stays dependency-free on Python 3.10+.

See [docs/task-contract.md](/homes/gws/tuxm/Project/auto-discovery/docs/task-contract.md) and [docs/skydiscover-math-inventory.md](/homes/gws/tuxm/Project/auto-discovery/docs/skydiscover-math-inventory.md).

## Related repos

`auto-discovery` borrows ideas from:

- [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch)
- [`skydiscover-ai/skydiscover`](https://github.com/skydiscover-ai/skydiscover)
- [`baidu-baige/LoongFlow`](https://github.com/baidu-baige/LoongFlow)
