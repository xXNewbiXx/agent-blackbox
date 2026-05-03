# Demo Pack — Agent Blackbox Safety Lab

Status: LOCAL_DRAFT

This is the smallest demo pack for the Safety Lab positioning:

1. Run report mock: an agent changes release/CI files.
2. Policy decision card: the run is blocked until human approval.
3. Replay value: command, changed files, risk hints, decision and next action are visible.

## Demo story in 30 seconds

> A coding agent looks successful, but it touched release automation and tried a push-like action. Agent Blackbox records the evidence and the policy gate turns the run into a clear BLOCK decision instead of silent trust.

## Artifacts to show

Use the current `.agent-blackbox/latest` report from a demo checkout:

- Run JSON: `.agent-blackbox/latest/run.json`
- Summary: `.agent-blackbox/latest/summary.md`
- Dashboard: `.agent-blackbox/latest/dashboard.html`
- Diff: `.agent-blackbox/latest/diff.patch`

For a public demo, create a fresh toy checkout run instead of publishing local machine paths.

## Real local evidence pattern

A credible local sandbox run should show:

- Exit code: `0` from the wrapped command
- Changed files: e.g. `CHANGELOG.md`, `.github/workflows/release.yml`
- Risk hints: e.g. `destructive_hint`, `file_write`, `network_hint`
- Policy decision: `block`

This validates the pitch with an actual local artifact: the agent run exits successfully, but the policy gate still blocks automatic trust because the output contains destructive/network-like signals and release-adjacent files.

## Boundary

This is a local draft/demo mock. It does not contact a customer, push code, post publicly, or claim full prevention.
