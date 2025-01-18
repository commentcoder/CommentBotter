from discord.ext import commands
from settings import SOCIALS


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {}

    @commands.hybrid_command()
    async def github(self, ctx):
        await ctx.send(SOCIALS["github"])

    @commands.hybrid_command()
    async def instagram(self, ctx):
        await ctx.send(SOCIALS["instagram"])

    @commands.hybrid_command()
    async def linkedin(self, ctx):
        await ctx.send(SOCIALS["linkedin"])

    @commands.hybrid_command()
    async def tiktok(self, ctx):
        await ctx.send(SOCIALS["tiktok"])

    @commands.hybrid_command()
    async def udemy(self, ctx):
        await ctx.send(SOCIALS["udemy"])

    @commands.hybrid_command()
    async def youtube(self, ctx):
        await ctx.send(SOCIALS["youtube"])
    

async def setup(bot):
    await bot.add_cog(Social(bot))
