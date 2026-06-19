import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.getcwd()))

from fastapi.testclient import TestClient
from backend.app.main import app


class GenerateAPITest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_basic(self):
        payload = {"prompt": "Say hello", "messages": [{"role":"user","text":"hi"}], "preferred": "openai"}
        r = self.client.post("/generate/", json=payload)
        self.assertEqual(r.status_code, 200)
        j = r.json()
        self.assertIn("provider", j)
        self.assertIn("response", j)


if __name__ == "__main__":
    unittest.main()
