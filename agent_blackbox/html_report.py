import html
import json
from pathlib import Path


def render_dashboard(run_dir: Path) -> Path:
    data = json.loads((run_dir / 'run.json').read_text(encoding='utf-8'))
    stdout = (run_dir / 'stdout.log').read_text(encoding='utf-8', errors='replace') if (run_dir / 'stdout.log').exists() else ''
    stderr = (run_dir / 'stderr.log').read_text(encoding='utf-8', errors='replace') if (run_dir / 'stderr.log').exists() else ''
    diff = (run_dir / 'diff.patch').read_text(encoding='utf-8', errors='replace') if (run_dir / 'diff.patch').exists() else ''
    changed = data.get('changed_files', [])
    badges = ''.join('<span class="badge">%s</span>' % html.escape(x) for x in data.get('risk_hints', [])) or '<span class="badge ok">clean</span>'
    changed_html = ''.join('<li><code>%s</code></li>' % html.escape(x) for x in changed) or '<li>none</li>'
    policy = data.get('policy_decision') or {'decision': 'not evaluated', 'reasons': []}
    policy_reasons = ''.join('<li>%s</li>' % html.escape(x) for x in policy.get('reasons', [])) or '<li>none</li>'
    values = {
        'rid': html.escape(data['run_id']),
        'cmd': html.escape(' '.join(data['command'])),
        'exit': str(data.get('exit_code')),
        'dur': str(data.get('duration_seconds')),
        'files': str(len(changed)),
        'add': str(data.get('diff_added', 0)),
        'rem': str(data.get('diff_removed', 0)),
        'badges': badges,
        'policy': html.escape(policy.get('decision', 'not evaluated')),
        'policy_reasons': policy_reasons,
        'changed': changed_html,
        'timeline': html.escape(json.dumps(data.get('timeline', []), indent=2)),
        'stdout': html.escape(stdout[-20000:]),
        'stderr': html.escape(stderr[-20000:]),
        'diff': html.escape(diff[-40000:]),
    }
    doc = '''<!doctype html><meta charset="utf-8"><title>Agent Blackbox</title><style>body{margin:0;background:#07090f;color:#e8eefc;font:14px/1.5 system-ui}header{padding:44px 6vw 18px}h1{font-size:64px;letter-spacing:-.06em;margin:0}.tag,.badge,code{color:#72f1b8}.grid{display:grid;grid-template-columns:360px 1fr;gap:18px;padding:20px 6vw}.card{background:#0f1420;border:1px solid #243044;border-radius:22px;padding:18px}.kpi{display:grid;grid-template-columns:1fr 1fr;gap:12px}.kpi div{background:#0b101a;border-radius:14px;padding:12px}.kpi b{display:block;font-size:26px}.badge{display:inline-block;border:1px solid #243044;border-radius:999px;padding:5px 9px;margin:3px}pre{background:#05070c;border:1px solid #243044;border-radius:14px;padding:14px;max-height:420px;overflow:auto;white-space:pre-wrap}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style><header><div class="tag">Flight recorder for local AI agents</div><h1>Agent Blackbox</h1><p>If you can’t replay what your agent did, you can’t trust it.</p></header><main class="grid"><section class="card"><h2>Run summary</h2><p><b>ID:</b> <code>__rid__</code></p><p><b>Command:</b> <code>__cmd__</code></p><div class="kpi"><div>Exit<b>__exit__</b></div><div>Duration<b>__dur__s</b></div><div>Files<b>__files__</b></div><div>Diff<b>+__add__/-__rem__</b></div></div><h3>Risk hints</h3>__badges__<h3>Policy decision</h3><p><b>__policy__</b></p><ul>__policy_reasons__</ul><h3>Changed files</h3><ul>__changed__</ul></section><section class="card"><h2>Timeline</h2><pre>__timeline__</pre><h2>stdout</h2><pre>__stdout__</pre><h2>stderr</h2><pre>__stderr__</pre><h2>diff.patch</h2><pre>__diff__</pre></section></main>'''
    for k, v in values.items():
        doc = doc.replace('__' + k + '__', v)
    out = run_dir / 'dashboard.html'
    out.write_text(doc, encoding='utf-8')
    return out
