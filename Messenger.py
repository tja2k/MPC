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

    async def deleteMessage(self, message, delay=0):
        await message.delete(delay=delay)

    async def c__showcfg(self, message):
        try:
            msg = self.config.getJSONString()
            await self.simpleMessage(message.author, msg)
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
            elif previewMessage == "place1s": await self.photochallenge_first_place(target, [867115647561629696])
            elif previewMessage == "place1m": await self.photochallenge_first_place(target, [867115647561629696, 770239659182915594])
            elif previewMessage == "place2s": pass
            elif previewMessage == "place2m": pass
            elif previewMessage == "place3s": pass
            elif previewMessage == "place3m": pass
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

    # TODO Change winner_ids to entries and get winner_ids from entries respectively
    async def photochallenge_first_place(self, target, winner_ids):
        # No winners -> Something went wrong
        if len(winner_ids) == 0:
            await self.simpleMessage(target, self.config.get("errors.messenger_no_winners_given"))
            return

        # Get winners in following format <@id> <- Discord will convert this into a "ping"
        winners_ping = ""
        for member_id in winner_ids:
            winners_ping += f"<@{member_id}> "

        embed = discord.Embed()

        # Choose the right messages depending on how many winners there are
        # Add the image if there is only one winner directly
        if len(winner_ids) > 1:
            title = self.config.get("messages.photochallenge_first_place_title_multi")
            msg = self.config.get("messages.photochallenge_first_place_msg_multi")

            #Get image
        else:
            title = self.config.get("messages.photochallenge_first_place_title_single")
            msg = self.config.get("messages.photochallenge_first_place_msg_single")

        # Insert winners in final message

        msg = msg.replace("{winners}", winners_ping)

        
        embed.title = title
        embed.description = msg
        color = self.config.get("cfg.embed_color")
        embed.color = discord.Color.from_rgb(color[0],color[1],color[2])
        await target.send(embed=embed)

    async def __sendRemainingPosts(self, target, messages):
        pass
        #For message in messages:
        # make embed with attachment linked
        # Write "By <@user_id> in the footer"


    