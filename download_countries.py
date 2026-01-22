import requests
import json
import os
from pathlib import Path

API_URL = "https://restcountries.com/v3.1/all?fields=cca2,name,flags,region"

OUTPUT_DIR = Path("output")
FLAGS_DIR = OUTPUT_DIR / "flags"
JSON_PATH = OUTPUT_DIR / "countries.json"

OUTPUT_DIR.mkdir(exist_ok=True)
FLAGS_DIR.mkdir(exist_ok=True)

print("Downloading countries JSON...")

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

print(f"Countries fetched: {len(data)}")

countries = []

for c in data:
    try:
        code = c["cca2"].lower()
        name = c["name"]["common"]
        region = c.get("region", "")
        flag_url = c["flags"]["png"]

        # Save clean country object
        countries.append({
            "code": code.upper(),
            "name": name,
            "region": region
        })

        # Download flag
        flag_path = FLAGS_DIR / f"{code}.png"

        if not flag_path.exists():
            print(f"Downloading flag: {code}")
            img = requests.get(flag_url, timeout=30)
            img.raise_for_status()

            with open(flag_path, "wb") as f:
                f.write(img.content)

    except Exception as e:
        print(f"Skipping country due to error: {e}")

# Save JSON
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(countries, f, ensure_ascii=False, indent=2)

print("Done!")
print(f"Saved {len(countries)} countries")
print(f"Flags stored in: {FLAGS_DIR}")
