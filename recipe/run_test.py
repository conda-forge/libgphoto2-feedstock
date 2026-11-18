"""Smoke test: load libgphoto2 and its drivers. No camera is required."""
import ctypes
import os
import sys

libdir = os.path.join(os.environ["PREFIX"], "lib")
ext = "dylib" if sys.platform == "darwin" else "so"


def load(name):
    matches = [f for f in os.listdir(libdir) if f == f"lib{name}.{ext}"]
    assert matches, f"lib{name}.{ext} not found in {libdir}"
    return ctypes.CDLL(os.path.join(libdir, matches[0]))


port = load("gphoto2_port")
gp = load("gphoto2")
gp.gp_context_new.restype = ctypes.c_void_p
gp.gp_abilities_list_load.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
gp.gp_abilities_list_count.argtypes = [ctypes.c_void_p]
port.gp_port_info_list_load.argtypes = [ctypes.c_void_p]
port.gp_port_info_list_count.argtypes = [ctypes.c_void_p]

context = gp.gp_context_new()

abilities = ctypes.c_void_p()
assert gp.gp_abilities_list_new(ctypes.byref(abilities)) == 0
assert gp.gp_abilities_list_load(abilities, context) == 0
models = gp.gp_abilities_list_count(abilities)
print("camera models supported:", models)
assert models > 1000, "camera drivers failed to load"

ports = ctypes.c_void_p()
assert port.gp_port_info_list_new(ctypes.byref(ports)) == 0
assert port.gp_port_info_list_load(ports) >= 0
count = port.gp_port_info_list_count(ports)
print("ports found:", count)
assert count > 0, "port drivers failed to load"
