# Configurations
import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Store configs in variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MOVES_API = "https://play.pokemonshowdown.com/data/moves.json"
DEX_API = "https://play.pokemonshowdown.com/data/pokedex.json"
NEWS_API = "https://pokemonshowdown.com/news.json"