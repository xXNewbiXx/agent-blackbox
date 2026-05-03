# Agent Blackbox Examples

These examples are local-first command wrappers. They do not log in, do not upload data, and do not contact Agent Blackbox servers. Replace the inner command with the agent or script you already run locally.

## Basic Python script

```bash
python3 -m agent_blackbox run -- python3 examples/tiny_agent.py
python3 -m agent_blackbox view
```

Use this to verify the toolchain before wrapping a real agent.

## Safe copy/paste rule

Run Agent Blackbox from the repository you want to inspect, and keep the wrapped command exactly as boring as the command you would have run manually. Do not pass production credentials, deploy tokens, or live service mutation commands into demo runs.

After every example below, open the local report:

```bash
python3 -m agent_blackbox view
```

## Codex CLI-style workflow

```bash
python3 -m agent_blackbox run -- codex "inspect this repo and propose one safe refactor"
python3 -m agent_blackbox view
```

What the report helps review:
- command that was executed
- stdout/stderr from the run
- files changed by the agent
- git diff after the run
- risk hints such as destructive commands, file writes, network-like output, or secret-like output

## Claude Code-style workflow

```bash
python3 -m agent_blackbox run -- claude "review this repo and suggest the smallest safe improvement"
python3 -m agent_blackbox view
```

Use the same pattern for any interactive or semi-interactive local agent launcher. Agent Blackbox records the command boundary and the repository state before/after the run; it does not impersonate the agent or log into external services for you.

## Aider-style workflow

```bash
python3 -m agent_blackbox run -- aider --message "add a failing test for the bug before fixing it"
python3 -m agent_blackbox view
```

Review the HTML report before accepting generated changes.

## OpenHands / local agent wrapper pattern

```bash
python3 -m agent_blackbox run -- ./run-local-agent.sh
python3 -m agent_blackbox view
```

This is useful when the agent has its own launcher script. Agent Blackbox observes the wrapper command and the repo diff afterwards.

For demos, keep `run-local-agent.sh` local and reviewable. A good script for a first public demo should run tests or mutate a toy file, not call production APIs or deploy anything.

## Plain local script pattern

```bash
python3 -m agent_blackbox run -- bash scripts/local-smoke-test.sh
python3 -m agent_blackbox view
```

This is the lowest-friction adoption path for teams that do not yet use a named coding agent. The value proposition is the same: one durable artifact containing command, output, diff, changed files, exit code, and risk hints.

## CI smoke-test pattern

```bash
python3 -m agent_blackbox run -- python3 -m unittest discover -s tests -v
python3 -m agent_blackbox view
```

This creates a run artifact that shows whether a verification command passed and what changed around it.

## Responsible-use boundary

Agent Blackbox is an accountability layer, not a sandbox guarantee. It helps humans and teams inspect what happened. Do not claim it prevents all harmful actions. For production-grade enforcement, pair it with policy gates, least-privilege sandboxes, approval workflows, and secret redaction.

## What to show in demos

A strong demo should answer four questions in under 30 seconds:

1. What command did the agent run?
2. What files changed?
3. What risks were detected?
4. Can I replay the evidence locally without trusting a SaaS dashboard?
