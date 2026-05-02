import unittest
from agent_blackbox.risk import risk_hints


class RiskHintsTest(unittest.TestCase):
    def test_file_write_hint(self):
        self.assertIn('file_write', risk_hints(['python', 'x.py'], '', '', ['README.md']))

    def test_secret_hint_from_output(self):
        self.assertIn('secrets_hint', risk_hints(['python'], 'token=abc', '', []))

    def test_network_hint_from_command(self):
        self.assertIn('network_hint', risk_hints(['curl', 'https://example.com'], '', '', []))


if __name__ == '__main__':
    unittest.main()
