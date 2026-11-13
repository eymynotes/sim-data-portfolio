# run to validate .usd asset

import re
import sys
from pathlib import Path
from pxr import Usd, Sdf, UsdGeom, UsdPhysics, UsdSemantics

ALLOWED_UP_AXES = ("Y", "Z")
EXPECTED_METERS_PER_UNIT = 1.0
NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

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
    bad = [str(p.GetPath()) for p in stage.Traverse()
           if not NAME_PATTERN.match(p.GetName())]
    if bad:
        return False, "invalid prim names: " + ", ".join(bad)
    root = stage.GetDefaultPrim()
    if root and not root.GetName()[0].isupper():
        return False, f"default prim '{root.GetName()}' should start with a capital letter"
    return True, "prim names are valid and the default prim is capitalized"


def check_physics_and_labels(stage):
    # Day 5: check shelf physics and labels
    issues = []
    root = stage.GetDefaultPrim()
    if not root:
        return False, "no valid defaultPrim"

    # Rigid body and mass on the root prim
    if not root.HasAPI(UsdPhysics.RigidBodyAPI):
        issues.append("Root has no RigidBodyAPI")
    if not root.HasAPI(UsdPhysics.MassAPI):
        issues.append("Root has no MassAPI")
    else:
        mass = UsdPhysics.MassAPI(root).GetMassAttr().Get()
        if not mass or mass <= 0:
            issues.append("Mass missing or not positive")

    # Collision on every mesh
    for prim in Usd.PrimRange(root):
        if prim.IsA(UsdGeom.Mesh) and not prim.HasAPI(UsdPhysics.CollisionAPI):
            issues.append(f"No CollisionAPI on {prim.GetPath()}")

    # Semantic label on the root prim
    if not root.HasAPI(UsdSemantics.LabelsAPI, "class"):
        issues.append("Root has no semantic label")
    else:
        labels = UsdSemantics.LabelsAPI(root, "class").GetLabelsAttr().Get()
        if not labels:
            issues.append("Semantic label is empty")

    if issues:
        return False, "; ".join(issues)
    return True, "physics (rigid body, mass, colliders) and semantic label present"

CHECKS = [
    ("defaultPrim", check_default_prim),
    ("units", check_units),
    ("upAxis", check_up_axis),
    ("naming", check_naming),
    ("physics_and_labels", check_physics_and_labels),
]


def run_checks(path):
    stage = Usd.Stage.Open(str(path))
    if stage is None:
        return [("open", False, "could not open the file")]
    results = []
    for name, check in CHECKS:
        try:
            ok, message = check(stage)
        except Exception as e:
            ok, message = False, f"check crashed: {e}"
        results.append((name, ok, message))
    return results


def validate(path):
    results = run_checks(path)
    for name, ok, message in results:
        print("PASS" if ok else "FAIL", name, "-", message)
    return all(ok for _, ok, _ in results)


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).exists():
        print("ERROR !!! Usage: python validate_asset.py <path to .usda file>")
        sys.exit(2)
    result = validate(sys.argv[1])
    print("RESULT:", "PASS" if result else "FAIL")
    sys.exit(0 if result else 1)

    # Note : sys.argv is the list of words you typed on the command line