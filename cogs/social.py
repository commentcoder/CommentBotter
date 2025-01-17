from discord.ext import commands

socials = {
    "youtube": "https://www.youtube.com/channel/UCEztUC2WwKEDkVl9c6oUoTw?sub_confirmation=1",
    "udemy": "https://www.udemy.com/user/thomas-collart/?referralCode=F0901265E01C7FDADABC",
    "tiktok": "https://www.tiktok.com/@commentcoder",
    "instagram": "https://www.instagram.com/commentcoder_com",
    "github": "https://github.com/commentcoder",
    "linkedin": "https://linkedin.com/in/thomascollart/"
}

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {}

    @commands.hybrid_command()
    async def github(self, ctx):
        await ctx.send(socials["github"])

    @commands.hybrid_command()
    async def instagram(self, ctx):
        await ctx.send(socials["instagram"])

    @commands.hybrid_command()
    async def linkedin(self, ctx):
        await ctx.send(socials["linkedin"])

    @commands.hybrid_command()
    async def tiktok(self, ctx):
        await ctx.send(socials["tiktok"])

    @commands.hybrid_command()
    async def udemy(self, ctx):
        await ctx.send(socials["udemy"])

    @commands.hybrid_command()
    async def youtube(self, ctx):
        await ctx.send(socials["youtube"])
    

async def setup(bot):
    await bot.add_cog(Social(bot))
