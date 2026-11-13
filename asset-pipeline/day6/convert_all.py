import argparse
from pathlib import Path
from convert_asset import fix_asset
from validate_asset import run_checks

parser = argparse.ArgumentParser(description="Convert raw USD assets into clean USD")
parser.add_argument("input_dir")
parser.add_argument("output_dir")
args = parser.parse_args()

out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)

results = {}
for f in sorted(Path(args.input_dir).glob("*.usd*")):
    target = out / (f.stem + ".usda")
    try:
        final = fix_asset(f, target)
        results[f.name] = run_checks(final)
    except Exception as e:
        results[f.name] = [("convert", False, str(e))]
        
print("\nSUMMARY")
for asset, checks in results.items():
    failed = [(n, m) for n, ok, m in checks if not ok]
    if not failed:
        print("PASS", asset)
    else:
        print("FAIL", asset)
        for n, m in failed:
            print(f"    - {n}: {m[:150]}")