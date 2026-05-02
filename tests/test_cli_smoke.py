import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliSmokeTest(unittest.TestCase):
    def test_cli_version(self):
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1])
        result = subprocess.run(
            [sys.executable, '-m', 'agent_blackbox', '--version'],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('agent-blackbox 0.1.0', result.stdout)

    def test_cli_records_run(self):
        with tempfile.TemporaryDirectory() as d:
            tmp_path = Path(d)
            script = tmp_path / 'agent.py'
            script.write_text("from pathlib import Path\nPath('out.txt').write_text('hi')\nprint('done')\n", encoding='utf-8')
            subprocess.run(['git', 'init'], cwd=tmp_path, check=True, stdout=subprocess.PIPE)
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1])
            result = subprocess.run([sys.executable, '-m', 'agent_blackbox', 'run', '--', sys.executable, str(script)], cwd=tmp_path, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0, result.stderr)
            runs = list((tmp_path / '.agent-blackbox' / 'runs').iterdir())
            self.assertTrue(runs)
            data = json.loads((runs[0] / 'run.json').read_text(encoding='utf-8'))
            self.assertEqual(data['exit_code'], 0)
            self.assertIn('file_write', data['risk_hints'])
            self.assertTrue((runs[0] / 'dashboard.html').exists())


if __name__ == '__main__':
    unittest.main()
