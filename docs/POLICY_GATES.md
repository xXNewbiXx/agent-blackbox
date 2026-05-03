# Policy Gates

Agent Blackbox is primarily an evidence recorder: it captures what a local agent or script did so humans and teams can review the run. Policy gates are the next thin layer on top of that evidence: small, explainable checks that decide whether a run is safe to auto-accept, needs review, or must be blocked by an external workflow.

This page is intentionally conservative. It does **not** claim that Agent Blackbox is a sandbox, EDR, or full prevention system.

## Minimal decision model

A useful v0 policy decision can be represented with three outcomes:

| Outcome | Meaning | Example trigger |
| --- | --- | --- |
| `allow` | Low-risk local run; normal review still possible. | Tests pass, no risky hints, expected files changed. |
| `review` | Human should inspect the HTML report and diff before accepting. | File writes, stderr output, package-manager output, large diff. |
| `block` | Do not auto-merge or auto-apply; require explicit approval or a stronger sandbox. | Secret-like output, destructive commands, unexpected network activity, production path mutation. |

The practical goal is not perfect prevention. The goal is to turn opaque agent execution into a visible decision point before changes are trusted.

## Example mapping from current risk hints

Current risk hints can already support a simple local policy:

```text
allow  = no risk hints and exit_code == 0
review = file_write OR stderr_output OR network_hint
block  = secrets_hint OR destructive_hint
```

This is deliberately easy to explain in a PR, CI artifact, or security review:

- `file_write`: the agent changed files; inspect the diff.
- `network_hint`: the command/output suggests network activity; verify intent.
- `secrets_hint`: output resembles credentials or tokens; treat artifacts as sensitive.
- `destructive_hint`: command/output suggests deletion, force operations, or irreversible changes.
- `stderr_output`: the run emitted errors or warnings; inspect before trusting results.

## CI / PR gate sketch

A future GitHub Actions or local CI wrapper could use `run.json` as evidence:

```bash
python3 -m agent_blackbox run -- python3 -m unittest discover -s tests -v
python3 examples/check_blackbox_policy.py "$(cat .agent-blackbox/latest)/run.json"
```

The example script prints a small JSON decision:

```json
{
  "schema": "agent-blackbox.policy-decision.v1",
  "run_id": "20260503T000000Z",
  "decision": "review",
  "reasons": ["review risk hint: file_write"]
}
```

Possible CI behavior:

1. Always upload or retain the Agent Blackbox artifact for maintainers.
2. Pass automatically only when the decision is `allow`.
3. Mark the job as neutral/manual-review when the decision is `review`.
4. Fail the job when the decision is `block`.

The policy script should be small, auditable, and repo-local. Teams can then tune thresholds without sending traces to a hosted service.

## Demo narrative

A credible demo should show three runs side by side:

1. **Clean test run** — `allow`: tests pass, no risky hints.
2. **Agent changed code** — `review`: changed files and diff are visible.
3. **Secret/destructive-looking output** — `block`: the report makes the risk obvious and prevents silent acceptance.

This frames Agent Blackbox as OSS infrastructure for accountable autonomy: the blackbox records evidence, and policy gates convert that evidence into a review workflow.

## Boundaries

Policy gates should be presented as defense-in-depth, not a safety guarantee.

They should be paired with:

- least-privilege workspaces,
- no production credentials in agent shells,
- approval workflows for deploys and destructive commands,
- secret redaction/scanning,
- tamper-evident or append-only artifact storage for stronger audit needs.

## Open questions for v0.2

- Should the first built-in command be `agent_blackbox policy <run.json>` or should policy stay as example scripts first?
- Which default outcome should `network_hint` receive: `review` or `block`?
- Should policy decisions be written into `summary.md` and `dashboard.html`?
- How should teams override policy for intentional high-risk maintenance tasks?
