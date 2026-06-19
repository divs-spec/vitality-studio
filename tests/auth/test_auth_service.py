import os
import unittest

# ensure imports use project root
import sys
sys.path.insert(0, os.path.abspath(os.getcwd()))

from backend.app import auth as authsvc


class AuthServiceTest(unittest.TestCase):
    def setUp(self):
        # use a temp users file to avoid interfering with local state
        self.users_file = os.path.join(os.getcwd(), "tests", "tmp_users.json")
        if os.path.exists(self.users_file):
            os.remove(self.users_file)
        os.environ["VITALITY_USERS_FILE"] = self.users_file

    def tearDown(self):
        if os.path.exists(self.users_file):
            os.remove(self.users_file)

    def test_create_and_authenticate(self):
        email = "alice@example.com"
        pwd = "password123"
        u = authsvc.create_user(email, pwd)
        self.assertIn("id", u)

        # duplicate creation should raise
        with self.assertRaises(Exception):
            authsvc.create_user(email, pwd)

        token = authsvc.authenticate_user(email, pwd)
        self.assertIsNotNone(token)

        uid = authsvc.verify_token(token)
        self.assertEqual(uid, u["id"])

    def test_invalid_login(self):
        token = authsvc.authenticate_user("noone@example.com", "x")
        self.assertIsNone(token)


if __name__ == "__main__":
    unittest.main()
