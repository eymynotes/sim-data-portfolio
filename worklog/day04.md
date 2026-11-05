# Day 4
- Did: learn composition Arcs
- Broke:

- Learned: creating composition arcs
https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/index.html

##### Layers : stores USD scene information
##### Sublayer: stack a whole file under another (Day 2), count as part of Local.
##### Reference: bring a file in under a prim. Good for reusing an asset.
##### Payload: like a reference, but it can be left unloaded to save memory. Good for heavy assets.
##### Inherits: a prim follows a “class” prim, so changing the class changes every prim that inherits it.
##### Specializes: like inherits, but the weakest arc, so it only fills gaps.
##### LIVRPS: the strength order, strongest to weakest: Local, Inherits, Variants, References, Payloads, Specializes.

Steps (day4)
1. create box.usda, extra_payload.usda, layer_low.usda
2. set stage / combine assets >> scene.usda
3. run check_arcs.py to see result of scene.usda