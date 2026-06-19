import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.getcwd()))

from backend.app.plugins.manager import PluginManager


class PluginManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.join(os.getcwd(), 'tests', 'tmp_plugins')
        if os.path.exists(self.tmp):
            # clean
            for root, dirs, files in os.walk(self.tmp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        os.makedirs(self.tmp, exist_ok=True)
        # create a sample plugin
        pdir = os.path.join(self.tmp, 'example')
        os.makedirs(pdir, exist_ok=True)
        with open(os.path.join(pdir, 'plugin.json'), 'w', encoding='utf-8') as f:
            f.write('{"name":"example","version":"0.1.0"}')

    def tearDown(self):
        if os.path.exists(self.tmp):
            for root, dirs, files in os.walk(self.tmp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            try:
                os.rmdir(self.tmp)
            except Exception:
                pass

    def test_discover_and_load(self):
        mgr = PluginManager(plugins_dir=self.tmp)
        discovered = mgr.discover()
        self.assertIn('example', discovered)
        meta = mgr.load_metadata('example')
        self.assertEqual(meta.get('name'), 'example')


if __name__ == '__main__':
    unittest.main()
