# Name Pending

Current name is "samur.py", a play on "ninja", the underlying build system.

# Goal

Would like a simple file format for building, inspired by cargo's `cargo.toml`.

We want at least the following options, with some suggesstions for defaults:
Compiler: gcc on Linux (maybe just 'c++'), MSVC on Windows, clang on MacOS
Linker: lld everywhere
Build modes:
  Release: Optimization flags, NDEBUG
  Debug: Default, DEBUG
Position-independent by default
Hidden visibility by default

Targets should look something like:

```toml
[target1]
kind = "staticlib"
include_dir = "include"
sources = ["source1.cpp", "source2.cpp"]
```

(Using CMake terminology for a second)
Include directories are 'public', sources are 'private'. Header-only is an 'interface'.

Eventually the goal is to have this hooked up to Conan directly
so that dependencies can be read in directly, and information can
be passed seamlessly between them.

# Running

Currently, examples can be run like so:
```
python3 samur.py test/01/build.toml
```
This produces the executable `test/01/build/main`.