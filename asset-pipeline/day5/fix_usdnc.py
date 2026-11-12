# This is for houdini apprentice fix (.usdnc) 
# attempting to convert .usdnc to .usd
# NOT WORKING - cannot open geo.usd, mtl.usd, payload.usd
# Need to run the "add_physics.py" under hython.exe

import sys, shutil
from pathlib import Path
from pxr import Sdf

folder = Path(sys.argv[1])

# copy every .usdnc file to a .usd file
for f in folder.glob("*.usdnc"):
    shutil.copy(f, f.with_suffix(".usd"))
    print("Copied", f.name)

# rewrite references from .usdnc to .usd inside every .usd file
for f in folder.glob("*.usd"):
    layer = Sdf.Layer.FindOrOpen(str(f))
    if layer is None:
        print("CANNOT OPEN:", f.name)
        continue
    text = layer.ExportToString()
    if ".usdnc" in text:
        layer.ImportFromString(text.replace(".usdnc", ".usd"))
        layer.Save()
        print("Fixed", f.name)
    else:
        print("OK (no change)", f.name)