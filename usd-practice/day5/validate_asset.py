# run to validate .usd asset

import re
import sys
from pathlib import Path
from pxr import Usd, UsdGeom

ALLOWED_UP_AXES = ("Y", "Z")
EXPECTED_METERS_PER_UNIT = 1.0
NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9_]*$")


def check_default_prim(stage):
    prim = stage.GetDefaultPrim()
    if not prim:
        return False, "no valid defaultPrim"
    return True, f"defaultPrim is {prim.GetPath()}"


def check_units(stage):
    if not stage.HasAuthoredMetadata("metersPerUnit"):
        return False, "metersPerUnit is not authored"
    mpu = UsdGeom.GetStageMetersPerUnit(stage)
    if mpu != EXPECTED_METERS_PER_UNIT:
        return False, f"metersPerUnit is {mpu}, expected {EXPECTED_METERS_PER_UNIT}"
    return True, f"metersPerUnit is {mpu}"


def check_up_axis(stage):
    if not stage.HasAuthoredMetadata("upAxis"):
        return False, "upAxis is not authored"
    axis = UsdGeom.GetStageUpAxis(stage)
    if axis not in ALLOWED_UP_AXES:
        return False, f"upAxis is {axis}, expected one of {ALLOWED_UP_AXES}"
    return True, f"upAxis is {axis}"


def check_naming(stage):
    bad = [
        str(p.GetPath())
        for p in stage.Traverse()
        if not NAME_PATTERN.match(p.GetName())
    ]
    if bad:
        return False, "names must start with a capital letter: " + ", ".join(bad)
    return True, "all prim names start with a capital letter"


CHECKS = [
    ("defaultPrim", check_default_prim),
    ("units", check_units),
    ("upAxis", check_up_axis),
    ("naming", check_naming),
]


def validate(path):
    stage = Usd.Stage.Open(str(path))
    all_ok = True
    for name, check in CHECKS:
        ok, message = check(stage)
        all_ok = all_ok and ok
        print("PASS" if ok else "FAIL", name, "-", message)
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).exists():
        print("ERROR !!! Usage: python validate_asset.py <path to .usda file>")
        sys.exit(2)
    result = validate(sys.argv[1])
    print("RESULT:", "PASS" if result else "FAIL")
    sys.exit(0 if result else 1)

    # Note : sys.argv is the list of words you typed on the command line