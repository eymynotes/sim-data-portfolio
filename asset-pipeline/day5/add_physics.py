# Physics script
import sys
from pxr import Usd, UsdGeom, UsdPhysics

def add_physics(path_in, path_out, mass_kg=25.0):
    stage = Usd.Stage.Open(path_in)
    root = stage.GetDefaultPrim()
    if not root:
        raise RuntimeError("No default prim. Fix the asset first.")

    # 1. Rigid body and mass go on the root prim
    UsdPhysics.RigidBodyAPI.Apply(root)
    UsdPhysics.MassAPI.Apply(root).CreateMassAttr(mass_kg)

    # 2. Collision goes on every mesh
    # Usd.PrimRange = walk through (iterate over) prims in a USD scene hierarchy
    count = 0
    for prim in Usd.PrimRange(root):
        if prim.IsA(UsdGeom.Mesh):
            UsdPhysics.CollisionAPI.Apply(prim)
            mc = UsdPhysics.MeshCollisionAPI.Apply(prim)
            mc.CreateApproximationAttr("convexHull")
            count += 1

    # Writes everything to a new file
    stage.GetRootLayer().Export(path_out)
    print(f"Added physics to {count} meshes. Saved {path_out}")

# call function
if __name__ == "__main__":
    add_physics(sys.argv[1], sys.argv[2])