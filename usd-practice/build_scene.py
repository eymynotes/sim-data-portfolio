# Use Python script to write USD

from pathlib import Path
from pxr import Usd, UsdGeom, Gf

# Create an empty Stage with Y-up and meters header
out = Path(__file__).parent / "built_scene.usda"
stage = Usd.Stage.CreateNew(str(out))

UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

# Add world and ground
world = UsdGeom.Xform.Define(stage, "/world")
stage.SetDefaultPrim(world.GetPrim())

ground = UsdGeom.Cube.Define(stage, "/world/Ground")
ground.GetSizeAttr().Set(1.0)
ground.AddTranslateOp().Set(Gf.Vec3d(0, -0.05, 0))
ground.AddScaleOp().Set(Gf.Vec3f(10, 0.1, 10))

##### "Define" : creates a prim at that Path
##### "AddTranslateOp", "AddScaleOp" : are "xformOp:translate" and "xformOp:scale" in usd

# Add 3 shelves using loop
for i in range(3):
    shelf = UsdGeom.Xform.Define(stage, f"/world/Shelf_{i}")
    shelf.AddTranslateOp().Set(Gf.Vec3d(i * 2 - 2, 1, 0))

    body = UsdGeom.Cube.Define(stage, f"/world/Shelf_{i}/Body")
    body.GetSizeAttr().Set(1.0)
    body.AddScaleOp().Set(Gf.Vec3f(1, 2, 0.4))

# Save and print prim tree
stage.Save()

for prim in stage.Traverse():
    depth = prim.GetPath().pathElementCount - 1
    print(" " * depth + prim.GetName(), prim.GetTypeName())

##### "Traverse()" : walks every prim on the stage. The indentation shows the hierarchy

# Print Attributes (Read data back out of stage)
for attr in stage.GetPrimAtPath("/world/Shelf_0").GetAttributes():
    print(attr.GetName(), attr.Get())