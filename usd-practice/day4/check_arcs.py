from pathlib import Path
from pxr import Usd

folder = Path(__file__).parent
stage = Usd.Stage.Open(str(folder / "scene.usda"), Usd.Stage.LoadNone)


def show(path, attr_name):
    prim = stage.GetPrimAtPath(path)
    if prim.HasAttribute(attr_name):
        print(path, attr_name, "=", prim.GetAttribute(attr_name).Get())
    else:
        print(path, attr_name, "= (missing)")


for p in [
    "/World/LocalWins",
    "/World/InheritBeatsRef",
    "/World/RefBeatsSpecialize",
    "/World/FromSublayer",
]:
    show(p, "color")

print("--- payload not loaded ---")
show("/World/PayloadDemo", "note")

stage.Load("/World/PayloadDemo")
print("--- payload loaded ---")
show("/World/PayloadDemo", "note")

# See which layer contribute
# Help debug why the value is wrong
attr = stage.GetPrimAtPath("/World/InheritBeatsRef").GetAttribute("color")
for spec in attr.GetPropertyStack():
    print(spec.layer.identifier, spec.path, spec.default)

# Check tree
for prim in stage.Traverse():
    depth = prim.GetPath().pathElementCount - 1
    print("  " * depth + prim.GetName())