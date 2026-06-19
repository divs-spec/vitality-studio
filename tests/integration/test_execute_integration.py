import os
import sys
import unittest
import shutil
import subprocess

sys.path.insert(0, os.path.abspath(os.getcwd()))

from execution_engine.orchestrator import run_in_container


def docker_available():
    try:
        subprocess.run(["docker", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False


class ExecuteIntegrationTest(unittest.TestCase):
    @unittest.skipUnless(docker_available(), "Docker not available on runner")
    def test_run_python_snippet(self):
        out, err, code = run_in_container('python', 'print(\"integration-42\")', timeout=20)
        self.assertEqual(code, 0)
        self.assertIn('integration-42', out)


if __name__ == '__main__':
    unittest.main()
