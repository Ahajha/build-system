from ninja import BIN_DIR
from ninja.ninja_syntax import Writer
import toml

import sys
import subprocess
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


def _call_ninja(args: list[str]) -> int:
    """
    Calls ninja as a subprocess with the specified arguments.

    :param args: Arguments to be passed to ninja

    :return: The return code of ninja
    """
    return subprocess.call([os.path.join(BIN_DIR, "ninja")] + args, close_fds=False)


def main(args):
    toml_data = toml.load(args[0])
    dirname = os.path.abspath(os.path.dirname(args[0]))

    build_folder = _make_build_folder(dirname)
    build_file = os.path.join(build_folder, "build.ninja")

    writer = Writer(output=open(build_file, "w"))

    writer.rule(name="cc", command="g++ -c $in -o $out")
    writer.rule(name="link", command="g++ -fuse-ld=lld $in -o $out")

    for target, info in toml_data.items():
        objects = []
        for source in info["sources"]:
            filename, _ = os.path.splitext(source)
            objects.append(os.path.join(build_folder, f"{filename}.o"))

        for cpp, obj in zip(info["sources"], objects):
            writer.build(outputs=obj,
                         rule="cc",
                         inputs=os.path.join(dirname, cpp)
                         )

        if info["kind"] == "executable":
            writer.build(outputs=target,
                         rule="link",
                         inputs=objects
                         )

    writer.close()

    code = _call_ninja(["-C", build_folder])
    if code != 0:
        raise SystemExit(code)


if __name__ == "__main__":
    main(sys.argv[1:])
