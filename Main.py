from discord import message
import Photochallenge
import MessageParser
import discord
import Token
import Config
import Messenger

#TODO
# Messenger finish announcements for now
# Add ShowConfig method that prints the current config to the console

client = discord.Client()
config = Config.Config("configuration.json")
messenger = Messenger.Messenger(config, client)
photochallenge = Photochallenge.Photochallenge(client, config, messenger)
messageParser = MessageParser.MessageParser(config, messenger, photochallenge)

@client.event
async def on_ready():

    config.load()
    messageParser.addCommand("set", config.c__set)
    messageParser.addCommand("cfg", messenger.c__showcfg)
    messageParser.addCommand("preview", messenger.c__preview)
    messageParser.addCommand("start", photochallenge.c__start)
    messageParser.addCommand("end", photochallenge.c__end)
    messageParser.addCommand("here", photochallenge.c__set_photochallenge_channel)
    print("Bot ready")




@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    await messageParser(message)
    

client.run(Token.TOKEN)