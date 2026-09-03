# SPDX-FileCopyrightText: 2016 Ole Martin Bjorndalen <ombdalen@gmail.com>
#
# SPDX-License-Identifier: MIT

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # Python 3.7 and lower
    import importlib_metadata

__version__ = "0.0.0.dev0"

try:
    __version__ = importlib_metadata.version("mido")
except importlib_metadata.PackageNotFoundError:
    # Package is not installed
    pass

def _version_tuple(value):
    """Return the numeric release components exposed by this bundled fallback."""
    release = value.split("+", 1)[0].split("-", 1)[0]
    parts = []
    for token in release.split("."):
        digits = "".join(ch for ch in token if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


version_info = _version_tuple(__version__)
