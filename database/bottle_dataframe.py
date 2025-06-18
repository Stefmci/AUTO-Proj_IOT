import os
import json
import pandas as pd

def load_bottle_dataframe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "..", "bottles.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    bottles = data["_default"]
    rows = []
    for key, entry in bottles.items():
        row = {
            "bottle_id": entry.get("bottle"),
            "final_weight": entry.get("final_weight"),
            "is_cracked": entry.get("is_cracked"),
            "drop_oscillation": entry.get("drop_oscillation"),
            "temperature": entry.get("temperature"),
        }
        dispenser = entry.get("dispenser", {})
        for color in ["red", "blue", "green"]:
            disp = dispenser.get(color, {})
            row[f"{color}_fill_level_grams"] = disp.get("fill_level_grams")
            row[f"{color}_vibration_index"] = disp.get("vibration-index")
            row[f"{color}_time"] = disp.get("time")
        rows.append(row)
    return pd.DataFrame(rows)

print(load_bottle_dataframe().head())

if __name__ == "__main__":
    df = load_bottle_dataframe()
    df.to_csv("bottle_data.csv", index=False)
    print("CSV exportiert: bottle_data.csv")