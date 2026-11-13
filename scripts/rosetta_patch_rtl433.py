# Make rtl_433_ESP's receiver task stack overridable with -Drtl_433_ReceiverTask_Stack.
# rtl_433_ESP v0.6.2 hardcodes 2048 bytes, which overflows on the ESP32-S3 at the
# first log line. Patches the downloaded library in .pio/libdeps before it is built,
# so the fix survives a fresh install (local or CI). Idempotent.
import re
from pathlib import Path

Import("env")

src = Path(env.subst("$PROJECT_LIBDEPS_DIR"), env.subst("$PIOENV"), "rtl_433_ESP", "src", "rtl_433_ESP.cpp")
if src.is_file():
    text = src.read_text()
    if "#ifndef rtl_433_ReceiverTask_Stack" not in text:
        patched, n = re.subn(
            r"^#define\s+rtl_433_ReceiverTask_Stack\s+(\d+)\s*$",
            r"#ifndef rtl_433_ReceiverTask_Stack\n#  define rtl_433_ReceiverTask_Stack    \1\n#endif",
            text,
            count=1,
            flags=re.M,
        )
        if n != 1:
            env.Exit("rosetta_patch_rtl433: rtl_433_ReceiverTask_Stack definition not found in %s" % src)
        src.write_text(patched)
        print("rosetta_patch_rtl433: patched %s" % src)
