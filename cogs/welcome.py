import json
import libsql_experimental as libsql
import os
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

WELCOME_CHANNEL_ID : int = int(os.getenv("WELCOME_CHANNEL_ID") or 1213811649665044611)
TURSO_URL : str = os.getenv("TURSO_URL") or ""
TURSO_TOKEN : str = os.getenv("TURSO_TOKEN") or ""

INVITE_XP = 50

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if not welcome_channel:
            return

        updated_invites = await member.guild.invites()
        old_invites = self.invites.get(member.guild.id, [])

        inviter = None
        invites_count = 0
        invite_time = None

        for updated_invite in updated_invites:
            for old_invite in old_invites:
                if updated_invite.id == old_invite.id and updated_invite.uses > old_invite.uses:
                    inviter = updated_invite.inviter
                    invites_count = updated_invite.uses
                    invite_time = updated_invite.created_at
                    break

        self.invites[member.guild.id] = updated_invites

        if inviter:
            conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
            cursor = conn.cursor()
            cursor.execute("SELECT invited_members FROM invites WHERE user_id = ? AND guild_id = ?", (str(inviter.id), str(member.guild.id)))
            result = cursor.fetchone()

            total_xp = result[0] if result else 0

            if result:
                invited_members = json.loads(result[0]) 
                if str(member.id) in invited_members:
                    await welcome_channel.send(f"{inviter.mention}, vous avez déjà invité {member.mention} !")
                    # conn.close()
                    return
                
                total_xp = result[0] if result else 0
                total_xp += INVITE_XP
                cursor.execute(
                    "UPDATE users SET total_xp = ? WHERE user_id = ? AND guild_id = ?",
                    (total_xp, str(member.id), str(member.guild.id))
                )
            else:
                cursor.execute(
                    "INSERT INTO users (user_id, guild_id, total_xp, level) VALUES (?, ?, ?, ?)",
                    (str(member.id), str(member.guild.id), total_xp, 0)
                )

            if result:
                invited_members.append(str(member.id))
            else:
                invited_members = [str(member.id)]

            cursor.execute("INSERT OR REPLACE INTO invites (user_id, guild_id, last_invite_time, invited_members) VALUES (?, ?, ?, ?)",
                           (str(inviter.id), str(member.guild.id), time.time(), json.dumps(invited_members)))
            # conn.commit()
            # conn.close()

            await welcome_channel.send(
                f"Bienvenue {member.mention} ! (Invité par {inviter.mention} qui a invité : {invites_count} membres)."
            )
        else:
            await welcome_channel.send(f"Bienvenue {member.mention} !")

    @commands.hybrid_command()
    async def invited(self, ctx, member: discord.Member):
        """Donne la liste des membres invités par un membre."""
        conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("SELECT invited_members FROM invites WHERE user_id = ? AND guild_id = ?", (str(member.id), str(ctx.guild.id)))
        result = cursor.fetchone()

        if result:
            invited_members = json.loads(result[0])
            if invited_members:
                invite_list = "\n".join([f"<@{user_id}>" for user_id in invited_members])
                await ctx.send(f"{member.mention} a invité les membres suivants :\n{invite_list}")
            else:
                await ctx.send(f"{member.mention} n'a invité aucun membre.")
        else:
            await ctx.send(f"Aucune invitation trouvée pour {member.mention}.")

        # conn.close()

async def setup(bot):
    await bot.add_cog(Welcome(bot))
