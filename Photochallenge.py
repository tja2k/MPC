import discord
import datetime

class Photochallenge:
    def __init__(self, client, config, messenger) -> None:
        self.client = client
        self.config = config
        self.messenger = messenger
        self.activeCooldowns = dict()

    # Gets called by MessageParser if message is not a command
    async def __call__(self, message):
        # Check if message is an entry -> pc_channel, pc_active
        # Check if message is valid entry -> Only one attachment, attachment is jpeg or png
        # Check if cooldown for author is expired
        if not self.__isEntry(message):
            return

        if not await self.__isValidEntry(message):
            await self.messenger.deleteMessage(message)
            await self.messenger.simpleMessage(message.author, self.config.get("errors.photochallenge_entry_not_valid"))
            return

        if await self.__hasActiveCooldown(message):
            await self.messenger.deleteMessage(message)

            msg = self.config.get("errors.photochallenge_active_cooldown")
            msg += " "
            msg += str(self.__getRemainingCooldown(message))
            await self.messenger.simpleMessage(message.author, msg)

            return


        print("is entry")


    # Starts a photochallenge
    async def c__start(self, message):

        if self.config.get("state.photochallenge_active"):
            msg = self.config.get("errors.photochallenge_challenge_already_started")
            msg += " "
            msg += self.config.get("state.photochallenge_start_time")
            await self.messenger.simpleMessage(message.author, msg)
            return
        #set pc_active to true
        #set challenge_channel_id
        #set startingtime
        self.config.update("state.photochallenge_active", True, False)
        self.config.update("state.photochallenge_start_time", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), False)
        #self.config.update("state.photochallenge_channel_id", message.channel.id,False)

        await self.messenger.photochallenge_announcement(self.config.get("state.photochallenge_channel_id"))
        

    # Ends a photochallenge
    async def c__end(self, message):
        # get winners
        # announce winners through messenger
        # reset state
        self.config.update("state.photochallenge_active", False, False)
        self.config.update("state.photochallenge_start_time", "", False)
        #self.config.update("state.photochallenge_channel_id", 0,False)

    async def c__set_photochallenge_channel(self, message):
        self.config.update("state.photochallenge_channel_id", message.channel.id, False)
        await self.messenger.simpleMessage(message.author, self.config.get("warning.photochallenge_channel_changed"))

    def __isEntry(self, message) -> bool:
        if not message.channel.id == self.config.get("state.photochallenge_channel_id"):
            return False

        return self.config.get("state.photochallenge_active")

    async def __isValidEntry(self, message) -> bool:
        if len(message.attachments) != 1:
            return False

        return message.attachments[0].content_type in ("image/jpeg", "image/png")

    async def __hasActiveCooldown(self, message) -> bool:
        #If user is in active cooldowns and cooldown is active
        if message.author.id in self.activeCooldowns:
            allowedAgain = self.activeCooldowns[message.author.id] + datetime.timedelta(
            seconds=self.config.get("cfg.photochallenge_entry_cooldown"))
            if datetime.datetime.utcnow() < allowedAgain:
                return True

        self.activeCooldowns[message.author.id] = datetime.datetime.utcnow()
        return False

    def __getRemainingCooldown(self, message):
        try:
            allowedAgain = self.activeCooldowns[message.author.id] + datetime.timedelta(
                seconds=self.config.get("cfg.photochallenge_entry_cooldown"))

            
                
            return allowedAgain.replace(microsecond=0) - datetime.datetime.utcnow().replace(microsecond=0)
        except KeyError:
            return datetime.timedelta(seconds=0)

        


