import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
  
    print(f'Message {user_message} by {username} on {channel}')
    
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print('Trying to send a message')
        await message.channel.send(f'Hello {username}!')
            
client.run(token)