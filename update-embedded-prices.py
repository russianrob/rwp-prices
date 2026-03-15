import json
import re

# Load fresh price data
with open('rwp-prices.json', 'r') as f:
    data = json.load(f)

# Read the script
with open('torn-rw-pricer.user.js', 'r') as f:
    script = f.read()

# Map of variable names to JSON keys
replacements = {
    'DEFAULT_WEAPON_PRICES': 'weaponPrices',
    'DEFAULT_BONUS_PRICES': 'bonusPrices',
    'DEFAULT_CLASS_PRICES': 'classPrices',
    'DEFAULT_ARMOUR_PRICES': 'armourPrices',
    'DEFAULT_ARMOUR_BONUS_PRICES': 'armourBonusPrices',
    'DEFAULT_ARMOUR_SET_PRICES': 'armourSetPrices',
    'DEFAULT_WEAPON_COMBO_PRICES': 'weaponComboPrices',
    'DEFAULT_ARMOUR_COMBO_PRICES': 'armourComboPrices',
    'DEFAULT_WEAPON_MAX_BONUS': 'weaponMaxBonus',
}

for var_name, json_key in replacements.items():
    if json_key not in data:
        print(f"SKIP: {json_key} not in JSON data")
        continue
    new_json = json.dumps(data[json_key], separators=(',', ':'))
    # Find the start of the variable declaration
    marker = 'var ' + var_name + ' = '
    start = script.find(marker)
    if start == -1:
        print(f"WARNING: Could not find {var_name}")
        continue
    # Find the semicolon at end of line
    val_start = start + len(marker)
    end = script.find(';\n', val_start)
    if end == -1:
        end = script.find(';', val_start)
    if end == -1:
        print(f"WARNING: Could not find end of {var_name}")
        continue
    script = script[:val_start] + new_json + script[end:]
    print(f"Replaced {var_name} ({len(new_json)} chars)")

with open('torn-rw-pricer.user.js', 'w') as f:
    f.write(script)

print("Done! Script updated.")
