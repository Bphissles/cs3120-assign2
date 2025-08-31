# Load the notebook JSON, add missing "state" keys in metadata.widgets, and save a fixed copy.
import json, os, copy

src = "hw/hw2/linear_regression_lab.ipynb"
dst = "hw/hw2/linear_regression_lab_fixed.ipynb"

with open(src, "r", encoding="utf-8") as f:
    nb = json.load(f)

md = nb.get("metadata", {})

changed = False

if "widgets" in md:
    widgets = md["widgets"]
    # Handle both dict- and list-shaped widgets metadata defensively
    if isinstance(widgets, dict):
        # Some structures have ids mapping to widget dicts
        for k, v in list(widgets.items()):
            if isinstance(v, dict) and "state" not in v:
                v["state"] = {}
                changed = True
    elif isinstance(widgets, list):
        for i, v in enumerate(widgets):
            if isinstance(v, dict) and "state" not in v:
                v["state"] = {}
                changed = True

# Also check if widgets metadata is empty/None; if so, remove it
if "widgets" in md and (md["widgets"] is None or md["widgets"] == {}):
    # Remove empty widgets section to be safe
    del md["widgets"]
    nb["metadata"] = md
    changed = True

# Save the fixed notebook (even if unchanged to create a copy)
with open(dst, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Fixed notebook saved:", os.path.basename(dst))
print("Changed:", changed)
