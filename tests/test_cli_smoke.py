import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliSmokeTest(unittest.TestCase):
    def _run_cli(self, argv, cwd=None):
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1])
        return subprocess.run(
            [sys.executable, '-m', 'agent_blackbox', *argv],
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_cli_version(self):
        result = subprocess.run(
            [sys.executable, '-m', 'agent_blackbox', '--version'],
            env={'PYTHONPATH': str(Path(__file__).resolve().parents[1]), **os.environ},
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
            result = self._run_cli(['run', '--', sys.executable, str(script)], cwd=tmp_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            runs = list((tmp_path / '.agent-blackbox' / 'runs').iterdir())
            self.assertTrue(runs)
            data = json.loads((runs[0] / 'run.json').read_text(encoding='utf-8'))
            self.assertEqual(data['exit_code'], 0)
            self.assertIn('file_write', data['risk_hints'])
            self.assertEqual(data['policy_decision']['decision'], 'review')
            self.assertTrue((runs[0] / 'dashboard.html').exists())
            summary = (runs[0] / 'summary.md').read_text(encoding='utf-8')
            dashboard = (runs[0] / 'dashboard.html').read_text(encoding='utf-8')
            self.assertIn('Policy decision: `review`', summary)
            self.assertIn('Policy decision', dashboard)
            self.assertIn('review risk hint: file_write', dashboard)
            self.assertIn('out.txt', data['changed_files'])
            diff = (runs[0] / 'diff.patch').read_text(encoding='utf-8')
            self.assertIn('+++ b/out.txt', diff)
            self.assertIn('+hi', diff)

    def test_cli_policy_command_exit_code_and_output(self):
        with tempfile.TemporaryDirectory() as d:
            tmp_path = Path(d)
            run_json = tmp_path / 'run.json'

            cases = [
                ({'run_id': 'allow-run', 'exit_code': 0, 'risk_hints': []}, 0, 'allow'),
                ({'run_id': 'review-run', 'exit_code': 0, 'risk_hints': ['file_write']}, 1, 'review'),
                ({'run_id': 'block-run', 'exit_code': 0, 'risk_hints': ['secrets_hint']}, 2, 'block'),
            ]

            for payload, expected_exit, expected_decision in cases:
                with self.subTest(expected_decision=expected_decision):
                    run_json.write_text(json.dumps(payload), encoding='utf-8')
                    result = self._run_cli(['policy', str(run_json)])
                    self.assertEqual(result.returncode, expected_exit, result.stderr)
                    decision = json.loads(result.stdout)
                    self.assertEqual(decision['decision'], expected_decision)
                    self.assertEqual(decision['run_id'], payload['run_id'])


if __name__ == '__main__':
    unittest.main()
