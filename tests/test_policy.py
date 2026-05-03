import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_blackbox.policy import decide_policy


class PolicyDecisionTest(unittest.TestCase):
    def test_allow_clean_successful_run(self):
        decision = decide_policy({'exit_code': 0, 'risk_hints': []})
        self.assertEqual(decision['decision'], 'allow')

    def test_review_file_write(self):
        decision = decide_policy({'exit_code': 0, 'risk_hints': ['file_write']})
        self.assertEqual(decision['decision'], 'review')

    def test_block_secret_hint(self):
        decision = decide_policy({'exit_code': 0, 'risk_hints': ['secrets_hint']})
        self.assertEqual(decision['decision'], 'block')

    def test_example_script_outputs_json_and_review_exit_code(self):
        with tempfile.TemporaryDirectory() as d:
            run_json = Path(d) / 'run.json'
            run_json.write_text(json.dumps({
                'run_id': 'demo',
                'exit_code': 0,
                'risk_hints': ['network_hint'],
            }), encoding='utf-8')
            result = subprocess.run(
                [sys.executable, 'examples/check_blackbox_policy.py', str(run_json)],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['decision'], 'review')
            self.assertEqual(payload['run_id'], 'demo')


if __name__ == '__main__':
    unittest.main()
