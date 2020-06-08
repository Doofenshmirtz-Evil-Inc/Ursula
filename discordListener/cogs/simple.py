import random
import logging

import discord

from discord.ext import commands


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/v0.16.12/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
https://discordpy.readthedocs.io/en/v0.16.12/api.html#event-reference
"""


class SimpleCog(commands.Cog):
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='info')
    async def info(self, ctx):
        """Custom help command"""
        embed = discord.Embed(title="Type !help command for more info on a command.",
                              description="You can also type !help category for more info on a category.", colour=discord.Colour.purple())
        embed.add_field(name='joined', value='Says when a member joined', inline=True)
        embed.add_field(name='perms', value='A simple command which checks a members Guild Permissions', inline=True)
        embed.add_field(name='top_role', value='Simple command which shows the members Top Role', inline=True)
        embed.add_field(name='add', value='A simple command which does addition on two integer values', inline=True)
        embed.add_field(name='choose', value='Chooses between multiple choices', inline=True)
        embed.add_field(name='info', value='Custom help command', inline=True)
        embed.add_field(name='me', value='A simple command which only responds to the owner of the bot', inline=True)
        embed.add_field(name='repeat', value='A simple command which repeats our input', inline=True)
        embed.add_field(name='roll', value='Rolls a dice in NdN format', inline=True)
        embed.add_field(name='Help', value='shows this message', inline=True)
        embed.set_footer(text="Command prefix is !, EX: !help")
        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(SimpleCog(bot))
