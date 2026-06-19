import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class HealthTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("status"), "ok")


if __name__ == "__main__":
    unittest.main()
