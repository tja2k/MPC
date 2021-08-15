import discord
from discord.errors import Forbidden, HTTPException


class Messenger:
    def __init__(self, config, client) -> None:
        self.config = config
        self.client = client

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

    async def c__preview(self, message):
        target = message.author

        try:
            args = message.content.split(" ")
            previewMessage = args[1].lower()

            if previewMessage == "announcement": await self.photochallenge_announcement(target)
            elif previewMessage == "place1": await self.photochallenge_first_place(target, [867115647561629696, 867115647561629696])
            elif previewMessage == "place2": pass
            elif previewMessage == "place3": pass
            else: await self.simpleMessage(target, self.config.get("errors.messenger_preview_does_not_exist"))

        except IndexError:
            await self.simpleMessage(target, self.config.get("errors.messenger_no_preview_selected"))


    async def photochallenge_announcement(self, target):

        color = self.config.get("cfg.embed_color")

        embed = discord.Embed()
        embed.title = self.config.get("messages.photochallenge_announcement_title")
        embed.description = self.config.get("messages.photochallenge_announcement_msg")
        embed.color = discord.Color.from_rgb(color[0],color[1],color[2])

        await target.send(embed=embed)

    async def photochallenge_first_place(self, target, winners):
        if len(winners) == 0:
            await self.simpleMessage(target, self.config.get("errors.messenger_no_winners_given"))
            return

    

        if len(winners) == 1:
            print(f"And the winner is <@{winners[0]}>" )

        elif len(winners) > 1:
            msg = self.config.get("messages.photochallenge_fist_place_title_multi")

            members = ""
            for member_id in winners:
                members += f"<@{member_id}> "

            msg = msg.replace("{winners}", members)
            
            await self.simpleMessage(target, msg)


    