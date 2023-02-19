import discord
from discord.ext import commands

class Greetings(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Greetings Cog Loaded.')

    @discord.slash_command(description = "Say hello to the bot.") # creates a prefixed command
    async def hello(self, ctx): # all methods now must have both self and ctx parameters
        await ctx.respond(f'Hey {ctx.author.mention}!')

    @discord.slash_command(description = "Say goodbye to the bot.") # we can also add application commands
    async def bye(self, ctx):
        await ctx.respond(f'Bye {ctx.author.mention}!')

    @discord.user_command(name = "Greet user.", description = "Say hello to the user.")
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')

    @discord.user_command(name="Account Creation Date", description = "Show account creation date for user")
    async def account_creation_date(self, ctx, member: discord.Member):  # user commands return the member
        await ctx.respond(f"{member.name}'s account was created on {member.created_at}.")

    @commands.Cog.listener() # we can add event listeners to our cog
    async def on_member_join(self, member): # this is called when a member joins the server
    # you must enable the proper intents
    # to access this event.
    # See the Popular-Topics/Intents page for more info
        await member.send(f'Welcome to the server {member.mention}!')

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Greetings(bot)) # add the cog to the bot