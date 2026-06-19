import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.getcwd()))

from execution_engine.orchestrator import run_in_container


class OrchestratorTest(unittest.TestCase):
    @patch('subprocess.run')
    def test_run_in_container_success(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = b'hello'
        mock_proc.stderr = b''
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        out, err, code = run_in_container('python', 'print("hi")', timeout=5)
        self.assertEqual(out, 'hello')
        self.assertEqual(err, '')
        self.assertEqual(code, 0)

    def test_unsupported_language(self):
        with self.assertRaises(ValueError):
            run_in_container('ruby', 'puts "x"')


if __name__ == '__main__':
    unittest.main()
