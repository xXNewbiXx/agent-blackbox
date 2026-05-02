# Run Artifact Schema

Agent Blackbox writes one directory per run:

`.agent-blackbox/runs/<run_id>/`

## Files

- `run.json` — machine-readable run metadata
- `summary.md` — human-readable summary
- `dashboard.html` — local HTML report
- `stdout.log` — captured stdout
- `stderr.log` — captured stderr
- `diff.patch` — git diff after the run
- `git-status-before.txt`
- `git-status-after.txt`

## Current schema

`agent-blackbox.run.v1`

## Important `run.json` fields

- `schema`
- `run_id`
- `command`
- `cwd`
- `exit_code`
- `duration_seconds`
- `changed_files`
- `risk_hints`
- `diff_added`
- `diff_removed`
- `timeline`
- `privacy`

## Privacy invariants

- No cloud upload by default.
- No background daemon.
- No autonomous execution.
- Secrets are not intentionally collected.
- Logs may still contain secrets emitted by the wrapped command, so artifacts should be treated as sensitive.

## Integration thesis

This schema is intentionally small and boring: it can be exported into CI artifacts, internal compliance evidence, security incident timelines, or future OpenTelemetry-style agent traces without depending on a hosted service.
