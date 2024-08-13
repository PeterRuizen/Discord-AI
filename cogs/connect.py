import discord
from discord.ext import commands
import settings


class NotOwner(commands.CheckFailure):
    ...

def is_owner():
    async def predicate(ctx):
        if ctx.author.id != settings.BOT_OWNER_ID:
            raise NotOwner("You are not the owner of this server.")
        return True
    return commands.check(predicate)



class Connection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send("Joining your channel")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == settings.BOT_OWNER_ID:
            if before.channel is not None and after.channel is None:
                if member.guild.voice_client:
                    await member.guild.voice_client.disconnect()
                    print("Bot has left the voice channel because the owner left.")

async def setup(bot):
    await bot.add_cog(Connection(bot))