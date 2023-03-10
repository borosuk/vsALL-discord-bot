import discord
import os
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file

token = os.getenv("TOKEN")

bot = discord.Bot()
cogs_list = [
    'greetings',
    'tools',
    'games'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

bot.run(token)