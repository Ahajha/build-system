# Describes an abstract builder class

from target import Target

from abc import ABC, abstractmethod
import os


class Builder(ABC):
    # Stored as absolute path
    # TODO is there a path library?
    _build_folder: str

    def __init__(self, build_folder: str):
        assert (os.path.isabs(build_folder))
        self._build_folder = build_folder

    @abstractmethod
    def add_target(self, target: Target):
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def build(self):
        ...
