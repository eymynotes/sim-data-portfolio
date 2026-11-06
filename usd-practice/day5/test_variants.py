# TEST switch variants by script

from pathlib import Path
from pxr import Usd, UsdShade

stage = Usd.Stage.Open(str(Path(__file__).parent / "shelf_asset.usda"))
vset = stage.GetPrimAtPath("/Shelf").GetVariantSets().GetVariantSet("color")
body = stage.GetPrimAtPath("/Shelf/Body")

print("variants:", vset.GetVariantNames())
for name in vset.GetVariantNames():
    vset.SetVariantSelection(name)
    mat, _ = UsdShade.MaterialBindingAPI(body).ComputeBoundMaterial()
    print(name, "->", mat.GetPath())