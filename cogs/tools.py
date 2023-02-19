import discord
from discord.ext import commands

# Name	    Usage	                                                                            Color
# Primary	discord.ButtonStyle.primary / discord.ButtonStyle.blurple	                        Blurple
# Secondary	discord.ButtonStyle.secondary / discord.ButtonStyle.grey / discord.ButtonStyle.gray	Grey
# Success	discord.ButtonStyle.success / discord.ButtonStyle.green	                            Green
# Danger	discord.ButtonStyle.danger / discord.ButtonStyle.red	                            Red
# Link	    discord.ButtonStyle.link / discord.ButtonStyle.url	                                Grey

class ToolButtons(discord.ui.View):

    def __init__(self, latency):
        self.latency = latency
        super().__init__()

    @discord.ui.button(label="Ping", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message(f"Pong! {self.latency}ms")

    @discord.ui.button(label="Pong", row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(f"Ping! {self.latency}ms")

class Tools(commands.Cog):

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tools Cog Loaded.')

    @discord.message_command(name="Get Message ID", description="Get the selected message id.")
    async def get_message_id(self, ctx, message: discord.Message):  # message commands return the message
        await ctx.respond(f"Message ID: `{message.id}`.")

    @discord.slash_command(name = "tools", description = "Quick tools menu") # Create a slash command
    async def tools(self, ctx):
        await ctx.respond("Pick a choice!", view=ToolButtons(round(self.bot.latency * 1000))) # Send a message with our View class that contains the button

    @discord.slash_command(name = "purge", description = "Clear all messages in this channel")
    @commands.has_any_role('Admin')
    async def purge(self, ctx, amount: int, member:discord.Member=None):
        # If a member was specified, delete messages only for that member
        if member!=None:
            messages=[]
            async for msg in ctx.channel.history(limit=amount):
                if len(messages) == amount:
                    break
                if msg.author.id == member.id:
                    messages.append(msg)

            await ctx.channel.delete_messages(messages)
            await ctx.respond(f"{len(messages)} message(s) from {member.mention} have been purged")
            return

        # otherise delete all messages for the given limit
        await ctx.respond("Purging messages")
        amount += 1
        await ctx.channel.purge(limit=amount)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Tools(bot)) # add the cog to the bot