from pxr import Usd

path = r"C:\Users\lali\git_projects\sim-data-portfolio\usd-practice\scene.usda"
stage = Usd.Stage.Open(path)
for prim in stage.Traverse():
    print(prim.GetPath(), prim.GetTypeName())