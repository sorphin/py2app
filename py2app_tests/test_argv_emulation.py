"""
Testcase for checking argv_emulation
"""
import sys
if (sys.version_info[0] == 2 and sys.version_info[:2] >= (2,7)) or \
        (sys.version_info[0] == 3 and sys.version_info[:2] >= (3,2)):
    import unittest
else:
    import unittest2 as unittest

import subprocess
import shutil
import time
import os
import signal

DIR_NAME=os.path.dirname(os.path.abspath(__file__))

if sys.version_info[0] == 2:
    def B(value):
        return value

else:
    def B(value):
        return value.encode('latin1')




class TestArgvEmulation (unittest.TestCase):
    py2app_args = []
    setup_file = "setup.py"
    open_argument = '/usr/bin/ssh'
    app_dir = os.path.join(DIR_NAME, 'argv_app')

    # Basic setup code
    #
    # The code in this block needs to be moved to
    # a base-class.
    @classmethod
    def setUpClass(cls):
        p = subprocess.Popen([
                sys.executable,
                    cls.setup_file, 'py2app'] + cls.py2app_args,
            cwd = cls.app_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True)
        lines = p.communicate()[0]
        if p.wait() != 0:
            print (lines)
            raise AssertionError("Creating basic_app bundle failed")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(os.path.join(cls.app_dir, 'build')):
            shutil.rmtree(os.path.join(cls.app_dir, 'build'))

        if os.path.exists(os.path.join(cls.app_dir, 'dist')):
            shutil.rmtree(os.path.join(cls.app_dir, 'dist'))

    #
    # End of setup code
    # 

    def test_basic_start(self):
        self.maxDiff = None
        path = os.path.join( self.app_dir, 'dist/BasicApp.app')

        p = subprocess.Popen(["/usr/bin/open",
            '-a', path])
        exit = p.wait()

        self.assertEqual(exit, 0)

        path = os.path.join( self.app_dir, 'dist/argv.txt')
        for x in range(5):
            time.sleep(1)
            if os.path.exists(path):
                break

        self.assertTrue(os.path.isfile(path))

        fp = open(path)
        data = fp.read().strip()
        fp.close()

        self.assertEqual(data.strip(), repr([os.path.join(self.app_dir, 'dist/BasicApp.app/Contents/Resources/main.py')]))

    def test_start_with_args(self):
        self.maxDiff = None
        path = os.path.join( self.app_dir, 'dist/BasicApp.app')

        p = subprocess.Popen(["/usr/bin/open",
            '-a', path, self.open_argument])
        exit = p.wait()

        self.assertEqual(exit, 0)

        for x in range(5):
            time.sleep(1)
            if os.path.exists(path):
                break

        path = os.path.join( self.app_dir, 'dist/argv.txt')
        self.assertTrue(os.path.isfile(path))

        fp = open(path)
        data = fp.read().strip()
        fp.close()

        self.assertEqual(data.strip(), repr([os.path.join(self.app_dir, 'dist/BasicApp.app/Contents/Resources/main.py'), self.open_argument]))

class TestArgvEmulationWithUrL (TestArgvEmulation):
    py2app_args = []
    setup_file = "setup-with-urlscheme.py"
    open_argument = 'myurl:mycommand'
    app_dir = os.path.join(DIR_NAME, 'argv_app')


if __name__ == "__main__":
    unittest.main()
