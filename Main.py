import CommandParser
import discord
import Token
import Config
import Messenger



@client.event
async def on_ready():
    print("Bot ready")


@client.event
async def on_message(message):
    pass
    

client.run(Token.TOKEN)