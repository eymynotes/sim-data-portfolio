# Day 6 (new)
- Did: 
# Download random 3D asset online (obj, fbx)
# Export those assets into .usd
# Use python script to clean up the model (check default prim, up axis, scale, pivot, metadata), add physics and semantics data >>> then validate

# Asset USD (before clean up) /asset-pipeline/day6/raw
# Asset USD (after clean up) /asset-pipeline/day6/out

# Run python "convert_all.py" over raw folder, convert asset to correct USD, validate and create new USD at out 
### (`python convert_all.py raw out`)

- Broke: 
# Script initially didn't detect light and camera object

- Learned: python commands to create USD file 
# Write python to batch clean up the assets