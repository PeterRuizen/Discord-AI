import random
import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="?", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command(
            help="This is help in full so how the ping command will be displayed",
            brief="The brief version of the help you'll see",
            description="The description, here follows the description of the command",
            enable=True,
            hidden=False
    )
    async def ping(ctx):
        """Ping the bot"""
        await ctx.send("Pong!")

    @bot.command()
    async def choice(ctx, *options):
        await ctx.send(random.choice(options))

    @bot.command(
            help="repeats what you say with a space in between, only two words",
            brief="repeats what you say",
            description="here follows the description of the command",
    )
    async def say(ctx, what = "WHAT?", why = "WHY?"):
        await ctx.send(what + " " + why)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()