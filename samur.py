from target import Target
from builder import Builder
from ninja_builder import NinjaBuilder

import toml

import sys
import os


def _make_build_folder(dirname: str) -> str:
    """
    Creates a build folder in the assumed location (next to the build description file).

    :param dirname: The directory where the build file is in.

    :return: The path to the build location.
    """
    build_folder = os.path.join(dirname, "build")
    if not os.path.exists(build_folder):
        os.mkdir(build_folder)
    return build_folder


def main(args):
    toml_data = toml.load(args[0])
    dirname = os.path.abspath(os.path.dirname(args[0]))

    build_folder = _make_build_folder(dirname)

    builder: Builder = NinjaBuilder(build_folder)
    for name, info in toml_data.items():
        builder.add_target(Target(name, dirname, info))

    builder.close()
    builder.build()


if __name__ == "__main__":
    main(sys.argv[1:])
