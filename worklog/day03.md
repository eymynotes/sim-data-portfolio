# Day 3
- Did: Create USDA files from PYTHON SCRIPT (build_scene.py)
- Broke:

- Learned: python commands to create USD file 
https://openusd.org/release/api/usd_geom_page_front.html

##### "Define" : creates a prim at that Path
##### "AddTranslateOp", "AddScaleOp" : are "xformOp:translate" and "xformOp:scale" in usd
##### "Traverse()" : walks through every prim in the scene, one by one, 
#####                so you can inspect or change them without knowing their paths in advance.
#####                >> Print scene hierarchy, Find prim by type/name, Bulk edit, Check scene for problem