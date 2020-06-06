import discord
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.message.author
        await ctx.channel.send(f'{member.display_name} joined on {member.joined_at}')

def setup(bot):
    bot.add_cog(MembersCog(bot))
