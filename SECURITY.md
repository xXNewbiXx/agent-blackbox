# Security and Responsible Use

Agent Blackbox is a local-first flight recorder for AI-agent and script execution.

## Security model

Agent Blackbox records what a user explicitly runs through the CLI. It does not:

- upload data to a cloud service
- run as a background spyware process
- start autonomous tasks on its own
- claim to prevent all harmful actions

## Sensitive data

Captured stdout, stderr, diffs, and file paths may contain sensitive information if the wrapped command emits or writes it. Treat `.agent-blackbox/` artifacts as potentially sensitive.

By default, `.agent-blackbox/` is ignored by this repository's `.gitignore`.

## Reporting security issues

Please report security issues privately before public disclosure.

Suggested report contents:

- affected version or commit
- reproduction steps
- expected behavior
- actual behavior
- potential impact

## Responsible use

Agent Blackbox is intended for accountability, auditability, debugging, compliance support, and safer local development workflows. It should not be used to secretly monitor users or collect credentials.
