from target import Target
from builder import Builder
from ninja_builder import NinjaBuilder

import toml

import sys
import os


def main(args):
    toml_data = toml.load(args[0])
    requires_info = {"requires": toml_data.pop("requires", {})}
    build_info = toml_data
    dirname = os.path.abspath(os.path.dirname(args[0]))

    build_folder = os.path.join(dirname, "build")
    reqs_info_cache = os.path.join(build_folder, "reqs_cache.toml")
    build_info_cache = os.path.join(build_folder, "build_cache.toml")

    if not os.path.exists(build_folder):
        # First build, cache the initial config
        os.mkdir(build_folder)
        deps_out_of_date = True
        build_info_out_of_date = True
    else:
        # Otherwise, re-read the cache and check for changes
        old_reqs_info = toml.load(reqs_info_cache)
        old_build_info = toml.load(build_info_cache)
        deps_out_of_date = old_reqs_info != requires_info
        build_info_out_of_date = old_build_info != build_info

    if deps_out_of_date:
        print("Dependencies out of date, repulling")
        with open(reqs_info_cache, "w") as f:
            toml.dump(o=requires_info, f=f)
    if build_info_out_of_date or deps_out_of_date:
        print("Build files out of date, rewriting")
        with open(build_info_cache, "w") as f:
            toml.dump(o=build_info, f=f)

        builder: Builder = NinjaBuilder(build_folder)
        for name, info in build_info.items():
            builder.add_target(Target(name, dirname, info))

        builder.close()

    NinjaBuilder.build(build_folder)


if __name__ == "__main__":
    main(sys.argv[1:])
