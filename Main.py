import discord
import Token

client = discord.Client()

@client.event
async def on_ready():
    print("Bot ready")


@client.event
async def on_message(message):
    if message.author.bot:
        return



    id = "<@770239659182915594>"
    await message.channel.send(f"Hallo {id}")


client.run(Token.TOKEN)