from discord.ext import commands, voice_recv
import discord
import settings

import wave

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
        self.summoned = False
        self.wave_sink = None

    @commands.command()
    @is_owner()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            
            wave_path = "test.wav"
            self.wave_sink = voice_recv.WaveSink(wave_path)

            vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            vc.listen(self.wave_sink)

            await ctx.send("Joining you in " + channel.name + ".")
            self.summoned = True
        else:
            await ctx.send("You are not connected to a voice channel.")
   

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == settings.BOT_OWNER_ID and self.summoned:
            voice_client = member.guild.voice_client
            text_channel = discord.utils.get(member.guild.text_channels, name="🤖-bot-commands")
            #when owner leaves channel, bot leaves channel
            if before.channel and not after.channel:
                if voice_client:
                    if self.wave_sink:
                        self.wave_sink.cleanup()
                        self.wave_sink = None
                    if text_channel:
                        await text_channel.send(f"Leaving {before.channel.name} because my summoner left.")
                    await voice_client.disconnect()
                    self.summoned = False
                    
            #when the owner moves to a different channel, the bot follows
            elif after.channel and (not before.channel or before.channel.id != after.channel.id):
                if voice_client:
                    await voice_client.move_to(after.channel)
                    
                    #await voice_client.channel.listen(self.wave_sink)
                    #!!!!!!needs start listening again here
                    if text_channel:
                        await text_channel.send(f"Think I wouldn't find you in {after.channel.name}?")
                    
async def setup(bot):
    await bot.add_cog(Connection(bot))