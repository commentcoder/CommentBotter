import os
from dotenv import load_dotenv
import libsql_experimental as libsql
import discord
from discord.ext import commands
from .migrations.create_db import create_turbo_db

load_dotenv()

AUTHORIZED_CHANNEL_ID : str = os.getenv("DEBUG_CHANNEL_ID") or ""
TURBO_URL: str = os.getenv("TURBO_URL") or ""
TURBO_TOKEN: str = os.getenv("TURBO_TOKEN") or ""

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.id == ctx.bot.owner_id:
            return True
        if ctx.author.guild_permissions.administrator:
            return True
        if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
            raise commands.CheckFailure(f"Cette commande ne peut être exécutée que dans le canal <#{AUTHORIZED_CHANNEL_ID}>.")
        raise commands.CheckFailure("Vous ne pouvez pas exécuter cette commande.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Vous ne pouvez pas exécuter cette commande.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def init_db(self, ctx):
        await ctx.send(f"Création de DB initialisée ! 🎉")
        create_turbo_db()
        await ctx.send(f"Base de donnée créée avec succès ! 🎉")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_xp(self, ctx, member: discord.Member, xp: int):
        """Ajoute de l'XP à un membre."""
        if xp <= 0:
            await ctx.send("Veuillez spécifier une quantité positive d'XP.")
            return

        conn = libsql.connect(database=TURBO_URL, auth_token=TURBO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("SELECT total_xp FROM users WHERE user_id = ? AND guild_id = ?", (str(member.id), str(ctx.guild.id)))
        result = cursor.fetchone()

        total_xp = result[0] if result else 0
        total_xp += xp

        if result:
            cursor.execute(
                "UPDATE users SET total_xp = ? WHERE user_id = ? AND guild_id = ?",
                (total_xp, str(member.id), str(ctx.guild.id))
            )
        else:
            cursor.execute(
                "INSERT INTO users (user_id, guild_id, total_xp, level) VALUES (?, ?, ?, ?)",
                (str(member.id), str(ctx.guild.id), total_xp, 0)
            )

        conn.commit()
        conn.close()

        await ctx.send(f"Ajouté {xp} XP à {member.mention}. Nouveau total : {total_xp} XP.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_xp(self, ctx, member: discord.Member, xp: int):
        """Retire de l'XP à un membre."""
        if xp <= 0:
            await ctx.send("Veuillez spécifier une quantité positive d'XP.")
            return

        conn = libsql.connect(database=TURBO_URL, auth_token=TURBO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("SELECT total_xp FROM users WHERE user_id = ? AND guild_id = ?", (str(member.id), str(ctx.guild.id)))
        result = cursor.fetchone()

        if not result:
            await ctx.send(f"{member.mention} n'a pas encore d'XP enregistré.")
            conn.close()
            return

        total_xp = max(0, result[0] - xp)

        cursor.execute(
            "UPDATE users SET total_xp = ? WHERE user_id = ? AND guild_id = ?",
            (total_xp, str(member.id), str(ctx.guild.id))
        )

        conn.commit()
        conn.close()

        await ctx.send(f"Retiré {xp} XP à {member.mention}. Nouveau total : {total_xp} XP.")


async def setup(bot):
    await bot.add_cog(Database(bot))
