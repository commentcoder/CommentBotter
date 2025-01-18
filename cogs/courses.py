import libsql_experimental as libsql
import discord
from discord.ext import commands
from settings import COURSES

class Courses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["formations"])
    async def cours(self, ctx):
        """Affiche la liste des cours disponibles."""
        embed = discord.Embed(
            title="Mes Cours Udemy",
            description="Découvrez mes cours pour apprendre à coder !",
            color=discord.Color.blue()
        )

        for course in COURSES:
            embed.add_field(
                name=course["name"],
                value=f"[Lien vers le cours]({course['url']})",
                inline=False
            )

        embed.set_footer(text="N'hésitez pas à me poser des questions si besoin !")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Courses(bot))
