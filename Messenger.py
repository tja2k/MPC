import discord
from discord.errors import Forbidden, HTTPException


class Messenger:
    def __init__(self, config) -> None:
        self.config = config

    async def simpleMessage(self, target, message):
        try:
            await target.send(message)
        
        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)


    async def embedMessage(self, target, message, title="", color=None):
        try:
            if color == None:
                color = self.config.get("cfg.embed_color")

            embed = discord.Embed()

            embed.description = message
            embed.title = title
            embed.color = discord.Color.from_rgb(color[0], color[1], color[2])

            await target.send(embed=embed)

        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)