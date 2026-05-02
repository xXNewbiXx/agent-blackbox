# Launch Pack

## One-liner

Agent Blackbox is a flight recorder for local AI agents: every command, file change, and risk hint, replayable.

## Polarizing posts

- If your AI agent doesn't have a blackbox, it shouldn't touch production.
- Agents without blackboxes are toys, not infrastructure.
- Don't give an AI write access before you can replay what it did.
- The future is not autonomous agents. The future is accountable agents.

## GitHub description

Flight recorder for local AI agents — command logs, diffs, risk hints, and replayable HTML reports.

## Topics

ai-agents, observability, agent-safety, developer-tools, audit-log, llmops, local-first, python, agentops, ai-safety

## Hacker News / Reddit draft

Title: Agent Blackbox: a local-first flight recorder for AI coding agents

Post:
I built a tiny Python tool for a problem I keep hitting with coding agents: after an agent run, I want to know exactly what happened.

Agent Blackbox wraps any local command and records stdout/stderr, git status before/after, changed files, git diff, exit code, duration, risk hints, and a replayable local HTML report.

The thesis: if an AI agent can run commands or mutate a repo, it needs a blackbox before it touches serious work.

Repo: https://github.com/xXNewbiXx/agent-blackbox

Looking for feedback from people using Claude Code, Codex CLI, Aider, OpenHands, Cursor-like workflows, or internal coding agents.

## LinkedIn/X draft

AI agents are getting write access faster than teams are getting observability.

So I built Agent Blackbox: a local-first flight recorder for AI agents.

It records:
- commands
- stdout/stderr
- git diffs
- changed files
- exit code/duration
- risk hints
- replayable HTML reports

Thesis: if your AI agent doesn't have a blackbox, it shouldn't touch production.

https://github.com/xXNewbiXx/agent-blackbox

## Demo checklist before public posting

- CI green on GitHub.
- README badge visible.
- Screenshot added: `docs/assets/dashboard.png`.
- `docs/RUN_SCHEMA.md` linked.
- `SECURITY.md` linked.
- Roadmap issues created.

## First integration targets

1. GitHub Action artifact/report mode.
2. Codex CLI wrapper example.
3. Claude Code wrapper example.
4. Aider wrapper example.
5. Redaction/tamper-evident log mode.
