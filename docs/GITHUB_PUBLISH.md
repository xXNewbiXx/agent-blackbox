# GitHub Publish: Agent Blackbox

## Niederschwelligster Weg

1. Öffne diesen vorbefüllten GitHub-Link:
https://github.com/new?name=agent-blackbox&description=Flight+recorder+for+local+AI+agents+%E2%80%94+command+logs%2C+diffs%2C+risk+hints%2C+and+replayable+HTML+reports.&visibility=public

2. Wenn GitHub dich fragt: einloggen/authorize.
3. Sichtbarkeit: Public.
4. Button klicken: Create repository.
5. Danach im lokalen Repo ausführen:

```bash
cd /home/basti/workspace/agent-blackbox
git remote add origin https://github.com/<DEIN_GITHUB_USERNAME>/agent-blackbox.git
git branch -M main
git push -u origin main
```

## Falls GitHub CLI gewünscht ist

Aktuell ist `gh` hier nicht installiert. Wenn du willst, kann Hermes später GitHub CLI installieren/konfigurieren. Für OAuth wäre der normale Weg:

```bash
gh auth login --web
```

Dann öffnet GitHub eine Browser-/Device-Flow-Seite. Keine Tokens im Chat posten.

## Repo-Metadaten

Description:
Flight recorder for local AI agents — command logs, diffs, risk hints, and replayable HTML reports.

Topics:
ai-agents, observability, agent-safety, developer-tools, audit-log, llmops, local-first, python

Launch Claim:
If your AI agent doesn't have a blackbox, it shouldn't touch production.
