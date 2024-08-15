# This file contains all synchronous dex-related functions

import requests
DEX_API = "https://play.pokemonshowdown.com/data/pokedex.json"

def fetch_dex_data():
    response = requests.get(DEX_API)
    if response.status_code == 200:
        return response.json()
    return {}

def process_typing(types):
    if not types:
        return "Unknown"
    return f"{types[0] and types[1]}" if len(types) > 1 else types[0]
    
def process_abilities(abilities):
    ab1 = abilities.get('0', 'N/A')
    ab2 = abilities.get('1') # Important to use .get() here since '1' and 'H' may not exist, returning None if so
    hidden = abilities.get('H', "N/A")
    
    ab_str = f"{ab1}"
    if ab2:
        ab_str += f" / {ab2}"
    
    hidden_str = ""
    if hidden:
        hidden_str += hidden
        
    return ab_str, hidden_str

def process_baseStats(baseStats):
    stats_str = "\n".join([f"*{stat.upper()}*: {value}" for stat, value in baseStats.items()]) # Join the stats together with a new line
    return stats_str

def get_dex_info(dex_data, mon):
    dex_info = dex_data.get(mon, {})
    
    if not dex_info:
        return {"name":"Unknown"}
    
    # Handle types & abilities
    types_str = process_typing(dex_info["types"])
    abilities, hidden_ability = process_abilities(dex_info['abilities'])
    baseStats_str = process_baseStats(dex_info["baseStats"])
    
    return {
        "name": dex_info.get("name", "Unknown"),
        "number": dex_info["num"],
        "types": types_str,
        "abilities": abilities,
        "hidden_ability": hidden_ability,
        "tier": dex_info["tier"],
        "baseStats": baseStats_str
    }
    