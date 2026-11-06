from pathlib import Path
from pxr import Usd

path = Path(__file__).parent / "scene.usda"
stage = Usd.Stage.Open(str(path))

for prim in stage.Traverse():
    print(prim.GetPath(), prim.GetTypeName())