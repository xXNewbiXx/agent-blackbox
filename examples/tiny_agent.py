from pathlib import Path

print('[agent] reading README.md')
readme = Path('examples/sample_repo/README.md')
text = readme.read_text(encoding='utf-8')

print('[agent] adding installation section')
if '## Installation' not in text:
    readme.write_text(
        text.rstrip() + '\n\n## Installation\n\nRun this project locally. This line was written by the demo agent.\n',
        encoding='utf-8',
    )

print('[agent] creating TODO.md')
Path('examples/sample_repo/TODO.md').write_text(
    '# TODO\n\n- Review this agent-created file before trusting it.\n',
    encoding='utf-8',
)
print('[agent] done')
