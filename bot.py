from discord import client
from discord.ext import commands
from sale_bot import begin_sales
from list_bot import begin_lists
from offer_list_bot import begin_offer_lists
from config import discord_bot_token

bot = commands.Bot(command_prefix='c!')

@bot.event
async def on_ready():
    bot.load_extension('openseabot')
    begin_sales()
    begin_lists()
    begin_offer_lists()
    print("Open Sea bot is now online")
    

bot.run(discord_bot_token)