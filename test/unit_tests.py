from samur import main

import unittest
import os
import shutil
import subprocess


def _build(test_number: str) -> str:
    """
    Builds the test project and returns a path to the build directory
    """
    test_dir = os.path.join("test", test_number)
    build_dir = os.path.join(test_dir, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    main([os.path.join(test_dir, "build.toml")])

    return build_dir


class TestBuildSystem(unittest.TestCase):
    def test_01(self):
        build_dir = _build("01")
        exe = os.path.join(build_dir, "test01")
        self.assertTrue(os.path.exists(exe))
        subprocess.call(exe)

    def test_02(self):
        build_dir = _build("02")
        exe = os.path.join(build_dir, "test02")
        self.assertTrue(os.path.exists(exe))
        subprocess.call(exe)

    def test_03(self):
        build_dir = _build("03")
        # exe = os.path.join(build_dir, "test02")
        # self.assertTrue(os.path.exists(exe))
        # subprocess.call(exe)


if __name__ == '__main__':
    unittest.main()
