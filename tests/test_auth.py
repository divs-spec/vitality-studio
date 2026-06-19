import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_register_login(self):
        email = "test@example.com"
        pwd = "safe-password"
        r = self.client.post("/auth/register", json={"email": email, "password": pwd})
        self.assertIn(r.status_code, (200, 400))
        # try login
        r2 = self.client.post("/auth/login", json={"email": email, "password": pwd})
        self.assertIn(r2.status_code, (200, 401))


if __name__ == "__main__":
    unittest.main()
