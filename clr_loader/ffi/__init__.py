import glob
import os
import shutil
import sys

import cffi

from . import hostfxr, mono, netfx

__all__ = ["ffi", "load_hostfxr", "load_mono", "load_netfx"]

ffi = cffi.FFI()

for cdef in hostfxr.cdef + mono.cdef + netfx.cdef:
    ffi.cdef(cdef)


def load_hostfxr(dotnet_root):
    hostfxr_name = _get_dll_name("hostfxr")
    hostfxr_path = os.path.join(dotnet_root, "host", "fxr", "?.*", hostfxr_name)

    for hostfxr_path in reversed(sorted(glob.glob(hostfxr_path))):
        try:
            return ffi.dlopen(hostfxr_path)
        except Exception:
            pass

    raise RuntimeError(f"Could not find a suitable hostfxr library in {dotnet_root}")


def load_mono(path=None, gc=None):
    # Preload C++ standard library, Mono needs that and doesn't properly link against it
    if sys.platform.startswith("linux"):
        ffi.dlopen("stdc++", ffi.RTLD_GLOBAL)

    if path is None:
        from ctypes.util import find_library

        path = find_library(f"mono{gc or ''}-2.0")
        if path is None:
            raise RuntimeError("Could not find libmono")

    return ffi.dlopen(path, ffi.RTLD_GLOBAL)


def load_netfx():
    if sys.platform != "win32":
        raise RuntimeError(".NET Framework is only supported on Windows")

    dirname = os.path.join(os.path.dirname(__file__), "dlls")
    if sys.maxsize > 2 ** 32:
        arch = "amd64"
    else:
        arch = "x86"

    path = os.path.join(dirname, arch, "ClrLoader.dll")

    return ffi.dlopen(path)


def _get_dll_name(name):
    if sys.platform == "win32":
        return f"{name}.dll"
    elif sys.platform == "darwin":
        return f"lib{name}.dylib"
    else:
        return f"lib{name}.so"
