import discord
from discord.ext import commands
from .botgames.crps import CRPSAcceptChallenge

class Games(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Games Cog Loaded.')

    @discord.slash_command(description = "Challenge everyone to a match of Crazy Rock Paper Scissors.") # we can also add application commands
    async def crps(self, ctx):
        await ctx.respond(f"Crazy Rock papers scissors challenge from {ctx.author.mention}", view=CRPSAcceptChallenge()) # Send a message with our View class that contains the button

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Games(bot)) # add the cog to the bot