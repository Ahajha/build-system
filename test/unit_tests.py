from samur import main

import unittest
import os
import shutil


class TestBuildSystem(unittest.TestCase):

    def test_example_builds(self):
        for dir in ["01", "02"]:
            test_dir = os.path.join("test", dir)
            build_dir = os.path.join(test_dir, "build")
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            main([os.path.join(test_dir, "build.toml")])


if __name__ == '__main__':
    unittest.main()
