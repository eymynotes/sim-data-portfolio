from pathlib import Path
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf

out = Path(__file__).parent / "shelf_asset.usda"
stage = Usd.Stage.CreateNew(str(out))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

root = UsdGeom.Xform.Define(stage, "/Shelf")
stage.SetDefaultPrim(root.GetPrim())

body = UsdGeom.Cube.Define(stage, "/Shelf/Body")
body.GetSizeAttr().Set(1.0)
body.AddScaleOp().Set(Gf.Vec3f(1, 2, 0.4))

colors = {
    "red": Gf.Vec3f(0.8, 0.1, 0.1),
    "green": Gf.Vec3f(0.1, 0.7, 0.2),
    "blue": Gf.Vec3f(0.1, 0.2, 0.8),
}

UsdGeom.Scope.Define(stage, "/Shelf/Materials")
materials = {}
for name, rgb in colors.items():
    mat_name = name.capitalize()
    mat = UsdShade.Material.Define(stage, f"/Shelf/Materials/{mat_name}")
    shader = UsdShade.Shader.Define(stage, f"/Shelf/Materials/{mat_name}/Surface")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(rgb)
    shader_out = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
    mat.CreateSurfaceOutput().ConnectToSource(shader_out)
    materials[name] = mat

vset = root.GetPrim().GetVariantSets().AddVariantSet("color")
for name in colors:
    vset.AddVariant(name)
    vset.SetVariantSelection(name)
    with vset.GetVariantEditContext():
        UsdShade.MaterialBindingAPI.Apply(body.GetPrim()).Bind(materials[name])
vset.SetVariantSelection("red")

stage.Save()
print("Saved", out)