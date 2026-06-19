import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))

from backend.app import storage


class StorageServiceTest(unittest.TestCase):
    def setUp(self):
        # use a temporary storage base
        self.tmp_base = os.path.join(os.getcwd(), "tests", "tmp_storage")
        if os.path.exists(self.tmp_base):
            # clean
            for root, dirs, files in os.walk(self.tmp_base, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        os.environ["VITALITY_STORAGE_BASE"] = self.tmp_base

    def tearDown(self):
        if os.path.exists(self.tmp_base):
            for root, dirs, files in os.walk(self.tmp_base, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            try:
                os.rmdir(self.tmp_base)
            except Exception:
                pass

    def test_save_load_delete(self):
        user = "u1"
        chat = {"title": "test chat"}
        chat_id = storage.save_chat(user, chat)
        self.assertTrue(chat_id)

        files = storage.list_chats(user)
        self.assertTrue(any(chat_id in f for f in files))

        data = storage.load_chat(user, chat_id)
        self.assertEqual(data.get("title"), "test chat")

        storage.append_message(user, chat_id, {"role": "user", "text": "hello"})
        data2 = storage.load_chat(user, chat_id)
        self.assertEqual(len(data2.get("messages", [])), 1)

        ok = storage.delete_chat(user, chat_id)
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
