import re
SECRET_PATTERNS=[re.compile(r'(?i)(api[_-]?key|secret|token|password|private[_-]?key)'),re.compile(r'sk-[A-Za-z0-9_-]{20,}'),re.compile(r'ghp_[A-Za-z0-9_]{20,}')]
NETWORK_PATTERNS=[re.compile(r'\b(curl|wget|Invoke-WebRequest|fetch\(|requests\.|http://|https://)\b',re.I)]
DESTRUCTIVE_PATTERNS=[re.compile(r'\b(rm\s+-rf|del\s+/|Remove-Item|format\s+|drop\s+database)\b',re.I)]
def risk_hints(command,stdout,stderr,changed_files):
    text=' '.join(command)+'\n'+stdout[-8000:]+'\n'+stderr[-8000:]+'\n'+'\n'.join(changed_files)
    hints=set()
    if changed_files: hints.add('file_write')
    if any(p.search(text) for p in SECRET_PATTERNS): hints.add('secrets_hint')
    if any(p.search(text) for p in NETWORK_PATTERNS): hints.add('network_hint')
    if any(p.search(text) for p in DESTRUCTIVE_PATTERNS): hints.add('destructive_hint')
    if stderr.strip(): hints.add('stderr_output')
    return sorted(hints)
