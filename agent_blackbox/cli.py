import argparse,json,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
from . import __version__
from .html_report import render_dashboard
from .risk import risk_hints
ROOT_DIR='.agent-blackbox'
def _run_git(args,cwd):
    try: return subprocess.run(['git',*args],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20).stdout
    except Exception: return ''
def _is_git_repo(cwd):
    try: return subprocess.run(['git','rev-parse','--is-inside-work-tree'],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=5).stdout.strip()=='true'
    except Exception: return False
def _changed_files(cwd):
    out=_run_git(['status','--porcelain','-uall'],cwd) if _is_git_repo(cwd) else ''
    return sorted({line[3:].strip() for line in out.splitlines() if line.strip()})
def _untracked_files(cwd):
    out=_run_git(['ls-files','--others','--exclude-standard'],cwd) if _is_git_repo(cwd) else ''
    return sorted(x for x in out.splitlines() if x.strip() and not x.startswith(ROOT_DIR+'/'))
def _untracked_diff(cwd):
    chunks=[]
    for rel in _untracked_files(cwd):
        path=Path(cwd)/rel
        if not path.is_file():
            continue
        try:
            text=path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            chunks.append(f"diff --git a/{rel} b/{rel}\nnew file mode 100644\n--- /dev/null\n+++ b/{rel}\n@@ binary file omitted @@\n")
            continue
        lines=text.splitlines()
        chunks.append(f"diff --git a/{rel} b/{rel}\nnew file mode 100644\n--- /dev/null\n+++ b/{rel}\n@@ -0,0 +1,{len(lines)} @@\n" + ''.join(f"+{line}\n" for line in lines))
    return '\n'.join(chunks)
def _diff_stats(diff):
    a=r=0
    for line in diff.splitlines():
        if line.startswith(('+++','---')): continue
        if line.startswith('+'): a+=1
        elif line.startswith('-'): r+=1
    return a,r
def command_run(argv):
    cwd=Path.cwd()
    if not argv.command: print('error: missing command after --',file=sys.stderr); return 2
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); run_dir=cwd/ROOT_DIR/'runs'/run_id; run_dir.mkdir(parents=True,exist_ok=True)
    before=_run_git(['status','--porcelain'],cwd); timeline=[{'t':time.time(),'event':'start','command':argv.command,'cwd':str(cwd)}]
    start=time.time(); proc=subprocess.run(argv.command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); duration=round(time.time()-start,3)
    timeline.append({'t':time.time(),'event':'process_exit','exit_code':proc.returncode,'duration_seconds':duration})
    (run_dir/'stdout.log').write_text(proc.stdout,encoding='utf-8',errors='replace'); (run_dir/'stderr.log').write_text(proc.stderr,encoding='utf-8',errors='replace')
    (run_dir/'git-status-before.txt').write_text(before,encoding='utf-8'); (run_dir/'git-status-after.txt').write_text(_run_git(['status','--porcelain'],cwd),encoding='utf-8')
    diff=_run_git(['diff','--',':!'+ROOT_DIR],cwd) if _is_git_repo(cwd) else ''
    if _is_git_repo(cwd):
        untracked=_untracked_diff(cwd)
        if untracked:
            diff = (diff + '\n' + untracked).strip() + '\n'
    (run_dir/'diff.patch').write_text(diff,encoding='utf-8')
    changed=[x for x in _changed_files(cwd) if not x.startswith(ROOT_DIR+'/')]; add,rem=_diff_stats(diff); hints=risk_hints(argv.command,proc.stdout,proc.stderr,changed)
    data={'schema':'agent-blackbox.run.v1','run_id':run_id,'command':argv.command,'cwd':str(cwd),'exit_code':proc.returncode,'duration_seconds':duration,'changed_files':changed,'risk_hints':hints,'diff_added':add,'diff_removed':rem,'timeline':timeline,'privacy':{'cloud_upload':False,'secrets_intentionally_recorded':False}}
    (run_dir/'run.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    summary=f"# Agent Blackbox Run {run_id}\n\n- Command: `{' '.join(argv.command)}`\n- Exit code: `{proc.returncode}`\n- Duration: `{duration}s`\n- Changed files: `{len(changed)}`\n- Risk hints: `{', '.join(hints) or 'clean'}`\n- Dashboard: `{run_dir/'dashboard.html'}`\n\n## Changed files\n"+'\n'.join(f'- `{f}`' for f in changed)+'\n'
    (run_dir/'summary.md').write_text(summary,encoding='utf-8'); dashboard=render_dashboard(run_dir); (cwd/ROOT_DIR/'latest').write_text(str(run_dir),encoding='utf-8')
    print(f'Agent Blackbox captured run: {run_id}'); print(f'Report: {run_dir/"summary.md"}'); print(f'Dashboard: {dashboard}'); print(f'Risk hints: {", ".join(hints) or "clean"}')
    return proc.returncode
def command_view(argv):
    cwd=Path.cwd(); run_dir=(cwd/ROOT_DIR/'runs'/argv.run) if argv.run else Path((cwd/ROOT_DIR/'latest').read_text(encoding='utf-8').strip())
    print(render_dashboard(run_dir)); return 0
def main(argv=None):
    parser=argparse.ArgumentParser(prog='agent-blackbox',description='Flight recorder for local AI agents')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('run'); p.add_argument('command',nargs=argparse.REMAINDER); p.set_defaults(func=command_run)
    v=sub.add_parser('view'); v.add_argument('--run'); v.set_defaults(func=command_view)
    args=parser.parse_args(argv)
    if getattr(args,'command',None) and args.command[:1]==['--']: args.command=args.command[1:]
    return args.func(args)
if __name__=='__main__': raise SystemExit(main())
