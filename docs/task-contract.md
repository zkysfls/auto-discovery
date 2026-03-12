# Task contract

Each task lives in its own directory under `tasks/`.

## Required files

- `task.json`
- `program.md`
- `evaluator.py`
- the mutable solution file referenced by `entry_file`

## Optional seed archive

Tasks can also include:

- `seeds/seed_index.tsv`
- one or more seed snapshot files under `seeds/`

The intended pattern is:

- one run edits only the task's active solution file
- multiple runs can still preserve different good starting points as seeds

Seed files should expose the same API as the task solution file so they can be copied into place for future runs.

Recommended `seed_index.tsv` columns:

```text
seed_id	status	score	sum_radii	validity	commit	parent_seed	seed_path	strategy
```

Notes:

- `seed_id`: stable human-readable identifier for the seed
- `status`: usually `active` or `archived`
- `commit`: commit where this seed snapshot was sourced from
- `parent_seed`: `-` for root seeds, otherwise the immediate ancestor seed id
- `seed_path`: path to the seed snapshot relative to the task directory
- `strategy`: one-line description of the construction family

## `task.json`

Required keys:

```json
{
  "name": "circle_packing",
  "domain": "math",
  "objective": "maximize",
  "entry_file": "solve.py",
  "evaluator_file": "evaluator.py",
  "primary_metric": "combined_score",
  "allowed_edit_paths": ["solve.py"]
}
```

Optional keys:

- `display_metrics`: numeric metrics to print after each run
- `timeout_sec`: evaluator-side timeout budget
- `description`: short human description
- `source`: where the task was imported from

## Evaluator contract

`evaluator.py` must define:

```python
def evaluate(program_path: str) -> dict:
    ...
```

The returned dict should contain the configured `primary_metric`. This mirrors the SkyDiscover evaluator shape, so imported math tasks can stay close to upstream.

## Mutation rule

The default rule is strict: Codex should only edit the files listed in `allowed_edit_paths`. For imported math tasks, that should usually be exactly one file.

## Result files

Recommended split:

- `run_history.tsv`: untracked append-only local run log
- `results.tsv`: tracked curated milestones for GitHub

This keeps the raw experiment loop cheap and conflict-free while still exposing meaningful progress on the main branch.

For tracked `results.tsv`, prefer human-readable task-specific columns over the generic runner schema when that makes the benchmark easier to understand. For example, a math task can show both normalized `score` and raw objective values such as `sum_radii`.
