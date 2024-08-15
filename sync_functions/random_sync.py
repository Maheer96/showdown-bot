# This file contains all synchronous functions related to the random team generator command

# Fetch all pokemon with the same tier
def same_tier(dex_data, tier):
    return [mon for mon, info in dex_data.items() if info.get('tier') and info.get('tier').lower() == tier]
   
    
    
