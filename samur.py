from ninja import ninja
from ninja.ninja_syntax import Writer
import toml

import sys
import os


def make_build_folder() -> str:
    """
    Creates a build folder in the assumed location (next to the build description file).
    Returns the path to the build location.
    """
    build_folder = os.path.join(os.path.dirname(sys.argv[1]), "build")
    if not os.path.exists(build_folder):
        os.mkdir(build_folder)
    return build_folder


if __name__ == "__main__":
    toml = toml.load(sys.argv[1])

    build_folder = make_build_folder()
    build_file = os.path.join(build_folder, "build.ninja")

    writer = Writer(output=open(build_file, "w"))

    writer.rule(name="cc", command="g++ -c $in -o $out")
    writer.rule(name="link", command="g++ -fuse-ld=lld $in -o $out")

    for target, info in toml.items():
        objects = []
        for source in info["sources"]:
            filename, _ = os.path.splitext(source)
            objects.append(f"{filename}.o")

        for cpp, obj in zip(info["sources"], objects):
            writer.build(outputs=obj,
                         rule="cc",
                         inputs=os.path.join("..", cpp)
                         )

        if info["kind"] == "executable":
            writer.build(outputs=target,
                         rule="link",
                         inputs=objects
                         )

    writer.close()

    sys.argv = ["", "-C", build_folder]
    ninja()
