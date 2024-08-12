from discord.ext import commands
import random

class Slapper(commands.Converter):
    use_nicknames: bool
    def __init__(self, *, use_nicknames) -> None:
        self.use_nicknames = use_nicknames

    async def convert(self, ctx, argument):
        someone = random.choice(ctx.guild.members)
        nickname = ctx.author
        if self.use_nicknames:
            nickname = ctx.author.nick

        return f"{nickname} slaps {someone} with {argument}"

@commands.group()
async def basics(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid group command passed...')

@basics.command(
    help="This is help in full so how the ping command will be displayed",
    brief="The brief version of the help you'll see",
    description="The description, here follows the description of the command",
    enable=True,
    hidden=False
)
async def ping(ctx):
    """Ping the bot"""
    await ctx.send("Pong!")

@basics.command()
async def choice(ctx, *options):
    await ctx.send(random.choice(options))

@basics.command(
    help="repeats what you say with a space in between, only two words",
    brief="repeats what you say",
    description="here follows the description of the command",
)
async def say(ctx, what = "WHAT?", why = "WHY?"):
    await ctx.send(what + " " + why)

@basics.command()
async def slap(ctx, reason: Slapper(use_nicknames=True)):
    await ctx.send(reason)

async def setup(bot):
    bot.add_command(basics)
    bot.add_command(ping)
    bot.add_command(choice)
    bot.add_command(say)
    bot.add_command(slap)
    