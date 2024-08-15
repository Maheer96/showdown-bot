# This file contains all synchronous move-related functions

import requests
from config import MOVES_API

def fetch_move_data():
    response = requests.get(MOVES_API)
    if response.status_code == 200:
        return response.json()
    return {}

# Define separate functions for values that have exceptions
def process_accuracy(accuracy):
    if accuracy == True:
        return "Can't miss."
    elif isinstance(accuracy, int) or isinstance(accuracy, float):
        return f"{accuracy}%"
    else:
        return "N/A"
    
def process_targeting(target):
    # Dictionary for the various targets
    target_map = {
        "adjacentFoe": "Adjacent foe.",
        "any": "Any Pokémon.",
        "allyTeam": "Your Party.",
        "adjacentAllyOrSelf": "Adjacent ally, or yourself.",
        "self": "Yourself.",
        "allySide": "Your side of the battlefield.",
        "allAdjacentFoes": "All foes adjacent to the pokémon.",
        "foeSide": "All foes on the battlefield.",
        "allies": "Allies.",
        "all": "Everyone.",
        "adjacentAlly": "Adjacent ally.",
        "normal": "Normal; May affect anyone adjacent to the user.",
        "allAdjacent": "All pokémon that are adjacent to the user.",
        "randomNormal": "This move affects any random one of the adjacent pokémon."
    }
    
    if target in target_map:
        return target_map[target]
    else:
        return f"Target: {target}"

def get_move_info(move_data, move_name):
    move_info = move_data.get(move_name, {})
    
    # Use helper functions for accuracy and target values
    accuracy = process_accuracy(move_info.get("accuracy", "N/A"))
    target = process_targeting(move_info.get("target", "N/A"))
    
    return {
        'name': move_info.get('name', 'Unknown Move'),
        'type': move_info.get('type', 'N/A'),
        'power': move_info.get('basePower', 'N/A'),
        'accuracy': accuracy,
        'target': target,
        'category': move_info.get('category', 'N/A'),
        'priority': move_info.get('priority', 'N/A'),
        'number': move_info.get('num','N/A'),
        'desc': move_info.get('desc', 'N/A')
    }
    
