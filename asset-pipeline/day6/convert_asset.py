import sys
import re
from pathlib import Path
from pxr import Usd, UsdGeom, Gf, UsdLux

def clean_name(name):
    name = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not name or name[0].isdigit():
        name = "_" + name
    return name[0].upper() + name[1:]

def rename_default_prim(stage, asset_name):
    root = stage.GetDefaultPrim()
    old_path = root.GetPath()
    new_name = clean_name(asset_name)
    if root.GetName() == new_name:
        return
    editor = Usd.NamespaceEditor(stage)
    editor.RenamePrim(root, new_name)
    editor.ApplyEdits()
    new_path = old_path.GetParentPath().AppendChild(new_name)
    stage.SetDefaultPrim(stage.GetPrimAtPath(new_path))
    print(f"  renamed: {old_path} -> {new_path}")
    
def fix_asset(path_in, path_out):
    stage = Usd.Stage.Open(str(path_in))

    # 0. Remove scene-only prims by type
    for prim in list(stage.Traverse()):
        if not prim.IsValid():
            continue  # already removed along with its parent
        path = prim.GetPath()
        type_name = prim.GetTypeName()
        if prim.IsA(UsdGeom.Camera) or type_name.endswith("Light"):
            stage.RemovePrim(path)
            print("  removed:", path, f"({type_name})")
    # remove empty Light_* groups left behind
    for prim in list(stage.Traverse()):
        if prim.IsValid() and prim.GetName().startswith("Light") and not prim.GetChildren():
            stage.RemovePrim(prim.GetPath())

    # remove empty groups left behind (Xforms with no children)
    changed = True
    while changed:
        changed = False
        for prim in list(stage.Traverse()):
            if not prim.IsValid():
                continue
            if prim.GetTypeName() == "Xform" and not prim.GetChildren():
                print("  removed empty:", prim.GetPath())
                stage.RemovePrim(prim.GetPath())
                changed = True
                break
                        
    # 1. Default prim
    root = stage.GetDefaultPrim()
    if not root:
        top = [p for p in stage.GetPseudoRoot().GetChildren()
               if p.IsA(UsdGeom.Xformable)]
        if not top:
            raise RuntimeError("No geometry found")
        root = top[0]
        stage.SetDefaultPrim(root)

    rename_default_prim(stage, Path(path_in).stem)
    root = stage.GetDefaultPrim()

    xf = UsdGeom.Xformable(root)
    old = xf.GetLocalTransformation()
    correction = Gf.Matrix4d(1.0)

    # 2. Up axis: Z-up to Y-up (rotate -90 degrees about X)
    if UsdGeom.GetStageUpAxis(stage) == "Z":
        rot = Gf.Matrix4d().SetRotate(Gf.Rotation(Gf.Vec3d(1, 0, 0), -90))
        correction = correction * rot
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # 3. Scale to meters
    mpu = UsdGeom.GetStageMetersPerUnit(stage)
    if mpu != 1.0:
        correction = correction * Gf.Matrix4d().SetScale(mpu)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)

    # 4. Pivot to floor-center. First apply scale and rotation, then measure.
    xf.MakeMatrixXform().Set(old * correction)
    cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
    box = cache.ComputeWorldBound(root).ComputeAlignedRange()
    mn, mx = box.GetMin(), box.GetMax()
    shift = Gf.Vec3d(-(mn[0] + mx[0]) / 2, -mn[1], -(mn[2] + mx[2]) / 2)
    move = Gf.Matrix4d().SetTranslate(shift)
    xf.MakeMatrixXform().Set(old * correction * move)

    final_path = Path(path_out).with_name(stage.GetDefaultPrim().GetName() + ".usda")
    stage.GetRootLayer().Export(str(final_path))
    print(f"Fixed {Path(path_in).name} -> {final_path.name}")
    return final_path

if __name__ == "__main__":
    fix_asset(sys.argv[1], sys.argv[2])