from discord.ext import commands
import discord
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
            await ctx.send("Joining you in " + channel.name + ".")
            #self.voice_clients[0].listen(discord.reader.UserFilter(ctx.author))
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == settings.BOT_OWNER_ID and before.channel and not after.channel:
                voice_client = member.guild.voice_client
                if voice_client:
                    text_channel = discord.utils.get(member.guild.text_channels, name="🤖-bot-commands")
                    if text_channel:
                        await text_channel.send(f"Leaving {before.channel.name} because my summoner left.")
                    await voice_client.disconnect()
                    
async def setup(bot):
    await bot.add_cog(Connection(bot))