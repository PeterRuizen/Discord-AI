import settings
import discord
import cogs.greetings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class NotOwner(commands.CheckFailure):
    ...

def is_owner():
    async def predicate(ctx):
        if ctx.author.id != ctx.guild.owner_id:
            raise NotOwner("You are not the owner of this server.")
        return True
    return commands.check(predicate)

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="?", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

    @bot.command()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")

    @bot.command()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")

    @bot.command()
    @is_owner()
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")  

    @unload.error
    async def unload_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("You are not the owner of this server.")  

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()