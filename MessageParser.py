import discord 


class MessageParser:
    def __init__(self, config, messenger) -> None:
        self.config = config
        self.commands = dict()
        self.messenger = messenger

    async def __call__(self, message):

        if self.__isCommand(message):
            if not self.__hasPermission(message):
                await self.messenger.simpleMessage(message.author, self.config.get("errors.commands_no_permission"))
                return

            try:
                self.commands[self.__getCommand(message)](message)
            except KeyError:
                await self.messenger.simpleMessage(message.author, self.config.get("errors.commands_does_not_exist"))
                
            return


    def __getCommand(self, message) -> str:
        try:
            return message.content.split(" ")[0][len(self.config.get("cfg.command_prefix")):]
        except IndexError as e:
            print(e)

    def __isCommand(self, message) -> bool:
        return message.content.startswith(self.config.get("cfg.command_prefix"))

    def __hasPermission(self, message) -> bool:
        return message.author.id in self.config.get("cfg.bot_allowed_users")

    def addCommand(self, commandName, func):
        self.commands[commandName] = func
        