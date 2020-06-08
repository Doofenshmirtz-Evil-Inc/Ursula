import random
import logging
import discord

from discord.ext import commands
from discord.guild import VoiceChannel


class CallCog(commands.Cog):
    """CallCog"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    

def setup(bot):
    bot.add_cog(CallCog(bot))
