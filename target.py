# Describes a build target

import os


def _list_or_singleton(value) -> list:
    """
    If value is a list, returns value, otherwise creates a singleton list with the value.
    """
    if type(value) == list:
        return value
    else:
        return [value]


class Target:
    name: str

    base_path: str

    kind: str  # TODO: enum

    # Agnostic of build directory
    output: str

    # Paths are relative to the base directory
    sources: list[str]
    # Not yet implemented, adding for future use
    public_sources: list[str]

    # Absolute paths
    include_dirs: list[str]
    # Not yet implemented, adding for future use
    private_include_dirs: list[str]

    defines: list[str]  # NYI
    private_defines: list[str]  # NYI

    flags: list[str]  # NYI
    private_flags: list[str]  # NYI

    def __init__(self, name: str, base_path: str, toml_data):
        """
        Initializes a target.

        :param name: The name of the target. The resulting output file is based on this name.
        :param base_path: The directory that the build file resides in. Given as absolute path.
        :param toml_data: The data read from a toml file describing the target.
        """
        assert (os.path.isabs(base_path))

        self.name = name

        self.base_path = base_path

        self.kind = toml_data["kind"]

        if self.kind == "executable":
            self.output = self.name
        elif self.kind == "staticlib":
            # TODO names for other platforms
            self.output = self.name + ".a"
        # TODO support for other types of libraries

        self.sources = _list_or_singleton(toml_data["sources"])

        # TODO public sources

        include_dirs = \
            _list_or_singleton(toml_data.get("include_dir", [])) + \
            _list_or_singleton(toml_data.get("include_dirs", []))

        self.include_dirs = [os.path.abspath(
            os.path.join(base_path, dir)) for dir in include_dirs]

        # TODO private include dirs

        # TODO defines

        # TODO flags
