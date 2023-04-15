# A builder that uses Ninja

from builder import Builder
from target import Target

from ninja import BIN_DIR
from ninja.ninja_syntax import Writer

import os
import subprocess


class NinjaBuilder(Builder):
    _writer: Writer

    def _write_rules(self):
        self._writer.variable(key="include_flags",
                              value=""
                              )
        self._writer.rule(name="cc",
                          depfile="$out.d",
                          command="g++ -MD -MF $out.d -c $in -o $out $include_flags"
                          )
        self._writer.rule(name="link",
                          command="g++ -fuse-ld=lld $in -o $out"
                          )

    def __init__(self, build_folder: str):
        """
        Initializes a Ninja builder.

        :param build_folder: Absolute path to the build folder
        """
        Builder.__init__(self, build_folder)

        build_file = os.path.join(build_folder, "build.ninja")
        self._writer = Writer(output=open(build_file, "w"))

        self._write_rules()

    def add_target(self, target: Target):
        include_dirs = ["-I " + dir for dir in target.include_dirs]
        for source in target.sources:
            self._writer.build(outputs=os.path.join(self._build_folder, source + ".o"),
                               rule="cc",
                               inputs=os.path.join(target.base_path, source)
                               )
            self._writer.variable(key="include_flags",
                                  value=include_dirs,
                                  indent=4
                                  )

        object_files = [os.path.join(
            self._build_folder, source + ".o") for source in target.sources]
        if target.kind == "executable":
            self._writer.build(outputs=os.path.join(self._build_folder, target.output),
                               rule="link",
                               inputs=object_files
                               )
        # TODO static lib archiving

    def close(self):
        self._writer.close()

    def build(self):
        args = ["-C", self._build_folder]
        code = subprocess.call(
            [os.path.join(BIN_DIR, "ninja")] + args, close_fds=False)
        if code != 0:
            raise SystemExit(code)
