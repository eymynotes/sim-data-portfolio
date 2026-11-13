# Add semantic labels (manual)
import sys
from pxr import Usd, UsdSemantics

def add_label(path_in, path_out, label, instance="class"):
    stage = Usd.Stage.Open(path_in)
    root = stage.GetDefaultPrim()
    if not root:
        raise RuntimeError("No default prim. Fix the asset first.")
    api = UsdSemantics.LabelsAPI.Apply(root, instance)
    api.CreateLabelsAttr().Set([label])
    stage.GetRootLayer().Export(path_out)
    print(f"Labeled {root.GetPath()} as '{label}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: hython add_labels.py <input> <output> <label>")
        sys.exit(2)
    add_label(sys.argv[1], sys.argv[2], sys.argv[3])