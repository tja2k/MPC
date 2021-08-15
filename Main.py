import MessageParser
import discord
import Token
import Config
import Messenger

# TODO 
# Command Parser
# MPC

client = discord.Client()
config = Config.Config("configuration.json")
messenger = Messenger.Messenger(config)
messageParser = MessageParser.MessageParser(config, messenger)

@client.event
async def on_ready():

    config.load()
    messageParser.addCommand("set", config.c__set)
    print("Bot ready")




@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    await messageParser(message)
    

client.run(Token.TOKEN)