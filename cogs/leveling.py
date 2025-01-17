import os
import time
import libsql_experimental as libsql
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

TURSO_URL: str = os.getenv("TURSO_URL") or ""
TURSO_TOKEN: str = os.getenv("TURSO_TOKEN") or ""


def calculate_level(total_xp):
    """Calcule le niveau et l'XP restante en fonction de l'XP totale."""
    base_xp = 100
    level = 0
    while total_xp >= base_xp:
        total_xp -= base_xp
        level += 1
        base_xp = int(base_xp * 1.05)
    return level, total_xp


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        guild_id = message.guild.id
        current_time = int(time.time())
        conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT total_xp, level, last_message_time FROM users WHERE user_id = ? AND guild_id = ?",
            (str(user_id), str(guild_id)),
        )
        result = cursor.fetchone()

        total_xp = result[0] if result else 0
        previous_level = result[1] if result else 0
        last_message_time = result[2] if result and result[2] else 0

        if current_time - last_message_time < 60:
            # conn.close()
            return

        total_xp += 1

        level, xp_in_level = calculate_level(total_xp)

        if not result:
            cursor.execute(
                "INSERT INTO users (user_id, guild_id, total_xp, level, last_message_time) VALUES (?, ?, ?, ?, ?)",
                (str(user_id), str(guild_id), total_xp, level, current_time),
            )
        else:
            cursor.execute(
                "UPDATE users SET total_xp = ?, level = ?, last_message_time = ? WHERE user_id = ? AND guild_id = ?",
                (total_xp, level, current_time, str(user_id), str(guild_id)),
            )

        conn.commit()
        # conn.close()

        if level > previous_level:
            await self.update_level_in_nickname(message.author, level)

    async def update_level_in_nickname(self, member: discord.Member, level: int):
        if not member.guild.me.guild_permissions.manage_nicknames:
            return

        current_nickname = member.display_name

        if "Niveau" in current_nickname:
            base_name = current_nickname.split("[Niveau")[0].strip()
        else:
            base_name = current_nickname

        new_nickname = f"{base_name} [Niveau {level}]"

        if current_nickname != new_nickname:
            try:
                await member.edit(nick=new_nickname)
            except discord.Forbidden:
                print(f"Impossible de modifier le pseudo de {member} (permissions insuffisantes).")

    @commands.hybrid_command()
    async def rank(self, ctx, member: discord.Member):
        """Donne le niveau d'un membre."""
        member = member or ctx.author
        conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT total_xp, level FROM users WHERE user_id = ? AND guild_id = ?
        """, (str(member.id), str(ctx.guild.id)))
        result = cursor.fetchone()

        if result is None:
            await ctx.send(f"{member.mention} n'a pas encore gagné d'XP.")
        else:
            xp, level = result
            await ctx.send(f"{member.mention} est au niveau {level} avec {xp} XP.")
        # conn.close()

    @commands.hybrid_command()
    async def levels(self, ctx):
        """Donne le classement des membres avec le plus gros niveau."""
        conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT user_id, level, total_xp FROM users WHERE guild_id = ?
        ORDER BY level DESC, total_xp DESC LIMIT 10
        """, (str(ctx.guild.id),))
        results = cursor.fetchall()

        print("results", results)

        if not results:
            await ctx.send("Le classement est vide.")
        else:
            leaderboard = "🏆 Classement des membres 🏆\n"
            for i, (user_id, level, xp) in enumerate(results, start=1):
                member = ctx.guild.get_member(int(user_id))
                leaderboard += f"{i}. {member.display_name if member else 'Inconnu'} - Niveau {level} ({xp} XP)\n"
            await ctx.send(leaderboard)

        # conn.close()


async def setup(bot):
    await bot.add_cog(Leveling(bot))
