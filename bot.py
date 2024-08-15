import requests
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from sync_functions.move_sync import *
from sync_functions.news_sync import *
from sync_functions.dex_sync import *
from sync_functions.random_sync import *
import random

# Load environment variables
load_dotenv()

# Retrieve environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1270878021804490864

# Bot will be summoned via "!" prefix, and intends to use all of Discord's features / contents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Create an "on ready" event when the bot is triggered
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(
        "Hello! This is your Showdown Bot! To get started, try out some of my commands:\n\n"
        "* `!moveinfo *move*` — to learn information on any move\n"
        "* `!news` — to get the latest news from the Pokémon world\n"
        "* `!pokemon *pokemon*` — to get information on any Pokémon\n"
        "* `!randomgen *tier*` — to obtain a random team under a certain [Smogon tier](https://www.smogon.com/ingame/battle/tiering-faq)\n\n"
        "To see this message again, use `!commands`."
    )

    
# Allow the user to see the introductory message again
@bot.command(name="commands")
async def show_commands(ctx):
    await ctx.send(
        "* `!moveinfo *move*` — to learn information on any move\n"
        "* `!news` — to get the latest news from the Pokémon world\n"
        "* `!pokemon *pokemon*` — to get information on any Pokémon\n"
        "* `!random gen *tier*` — to obtain a random team under a certain [Smogon tier](https://www.smogon.com/ingame/battle/tiering-faq)\n\n"
    )

# Define a command that provides the information of a specified move
@bot.command(name='moveinfo')
async def move_info(ctx, *, move_name: str = None):
    # Assign move_data variable to the API json
    move_data = fetch_move_data()
    
    if move_name is None:
        random_move = random.choice(list(move_data.keys())) # Select a random move
        await ctx.send(f"Please provide a move name after the command, like `!moveinfo {random_move}`.")
        return  
    
    # Remove blank spaces to match api notation
    move_name = move_name.lower().replace(' ', '')
    # Access move information
    move_info = get_move_info(move_data, move_name)
    
    if move_info['name'] != 'Unknown Move':
        # Create a Discord Embed
        embed = discord.Embed(
            title=f"**{move_info['name']}**",
            description=f"{move_info['desc']}",
            color=discord.Color.blue()
            )
        embed.add_field(name="Type", value=move_info['type'], inline=True)
        embed.add_field(name="Power", value=move_info['power'], inline=True)
        embed.add_field(name="Accuracy", value=move_info['accuracy'], inline=True)
        embed.add_field(name="Target", value=move_info['target'], inline=True)
        embed.add_field(name="Category", value=move_info['category'], inline=True)
        embed.add_field(name="Priority", value=move_info['priority'], inline=True)
        embed.add_field(name='Move Number', value=move_info['number'], inline=True)
        
        # Send embed to the channel with embed argument set to our embed
        await ctx.send(embed=embed)
        
    else:
        await ctx.send(f"There is no information available on the move '{move_name}.' Please check for spelling or try again later.")
        
# Define a command to provide the latest Pokemon news
@bot.command(name='news')
async def news(ctx):
    # Load the most recent news and iterate through them
    news = fetch_news_data()
    
    embed = discord.Embed(
        title="Latest Pokémon Showdown News",
        color=discord.Color.blue()        
    )
    
    # Check if news exists in the first place
    if not news:
        await ctx.send("No news available at the moment.")
    
    for article in news:
        # Convert HTML links to Markdown format (see news_sync.py)
        summary = convert_html_links(article.get("summaryHTML", "No summary available."))
        # Clean up any remaining HTML tags
        summary = clean_html(summary)
        
        embed.add_field(
            name=article['title'],
            value=summary,
            inline=False
        )
    
    await ctx.send(embed=embed)
    
# Define a command to provide information on a specified pokemon    
@bot.command(name='pokemon')        
async def dex_info(ctx, *, mon: str = None):
    dex_data = fetch_dex_data()
    
    # Check if a Pokémon name was provided
    if mon is None:
        random_mon = random.choice(list(dex_data.keys())) # Select a random mon
        await ctx.send(f"Please provide a Pokémon's name after the command, like `!pokemon {random_mon}`.")
        return
    
    mon = mon.lower().replace(' ', '')
    mon_info = get_dex_info(dex_data, mon)
    
    if mon_info['name'] != 'Unknown':
        embed = discord.Embed(
            title=f"{mon_info['name']} - #{str(mon_info['number']).zfill(4)}", # Turn dex number into #XXXX format
            color=discord.Color.blue()
        )
        embed.add_field(name="Type(s)", value=mon_info['types'], inline=True)
        embed.add_field(name="Abilities", value=mon_info['abilities'], inline=True)
        embed.add_field(name="Hidden Ability", value=mon_info['hidden_ability'], inline=True)
        embed.add_field(name="Tier", value=mon_info['tier'], inline=True)
        embed.add_field(name="Base Stats", value=mon_info['baseStats'], inline=False)
        
        await ctx.send(embed=embed)
    
    else:
         await ctx.send(f"There is no information available on the Pokémon '{mon}.' Please check for spelling or try again later.")
        
# Define a command to randomly generate a team of six mons for a specified tier
@bot.command(name='randomgen')
async def random_gen(ctx, *, tier: str = None):
    dex_data = fetch_dex_data()
    
    # Manually set tiers since there is only a handful
    tiers = [
    "AG", "CAP", "CAP LC", "CAP NFE", "Illegal", "LC", "NFE", "NU", 
    "NUBL", "OU", "PU", "PUBL", "RU", "RUBL", "UU", "UUBL", "Uber", 
    "Unknown", "ZU", "ZUBL"
    ]
    
    if not tier:
        random_tier = random.choice(tiers)
        await ctx.send(f"Please specify a tier after the command, like `!randomgen {random_tier}`.")
        return
    
    # Convert to capital non-sensitive
    tier = tier.lower()
    tiers_lower = [t.lower() for t in tiers]
        
    if tier in tiers_lower:
        pokemon_same_tier = same_tier(dex_data, tier)
        
        if len(pokemon_same_tier) >= 6:
            random_gen = random.sample(pokemon_same_tier, 6)
            
            embed = discord.Embed(
                title=f"Random Team for Tier {tier.upper()}",
                color=discord.Color.blue()
            )
            
            for pokemon in random_gen:
                mon_info = get_dex_info(dex_data, pokemon)
                embed.add_field(
                    name=f"{mon_info['name']} - #{str(mon_info['number']).zfill(4)}",
                    value="",
                    inline=True
                )
                
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"There are not enough Pokémon in the tier '{tier}' to generate a team.")
            
    else:
        await ctx.send(f"Invalid tier '{tier}'. Please try again with a valid tier.")

bot.run(BOT_TOKEN)