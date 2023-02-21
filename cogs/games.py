import discord
from discord.ext import commands
from .botgames.crps import *
import vsalldb

leaderboards = {
    'crps': 'Crazy Rock Paper Scissors'
}

class Games(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.conn = vsalldb.get_connection()
        self.curs = self.conn.cursor()
        super().__init__()

    def leaderboardSelection():
        leaderboardSelection = discord.Option(
                str,
                name = "game",
                description = "Which game?",
                choices = {formatChoice(v, k) for (k, v) in leaderboards.items()},
                required = True,
                min_values = 1,
                max_values = 1
            )
        
        return leaderboardSelection

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CRPSAcceptChallenge(None)) # Registers a View for persistent listening
        print('Games Cog Loaded.')

    @discord.slash_command(description = "Challenge everyone to a match of Crazy Rock Paper Scissors.") # we can also add application commands
    async def crps(self, ctx, selection: getSelection()):
        await ctx.respond(f"Crazy Rock papers scissors challenge from {ctx.author.mention}", view=CRPSAcceptChallenge(selection)) # Send a message with our View class that contains the button

    @discord.slash_command(description = "Check leaderboards")
    async def leaderboard(self, ctx, selection: leaderboardSelection()):
        embed = discord.Embed(
            title = leaderboards[selection],
            description = "Leaderboard values",
            color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        sqlquery = f"SELECT PLAYER1, PLAYER2 FROM GAMES_CRPS"
        result = self.curs.execute(sqlquery)

        player1 = {item[0] for item in result}
        player2 = {item[1] for item in result}

        embed.add_field(name = "Player 1", value = f"{player1}", inline = True)
        embed.add_field(name = "Player 2", value = f"{player2}", inline = True)

        embed.set_footer(text="by DarXyde") # footers can have icons too
        embed.set_author(name="vsALL") # , icon_url="https://example.com/link-to-my-image.png")
        
        await ctx.respond("Here is the leaderboard requested!", embed=embed) # Send the embed with some text

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Games(bot)) # add the cog to the bot

