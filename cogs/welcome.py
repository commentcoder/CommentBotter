import json
import libsql_experimental as libsql
import os
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

WELCOME_CHANNEL_ID : str = os.getenv("WELCOME_CHANNEL_ID") or ""
TURBO_URL : str = os.getenv("TURBO_URL") or ""
TURBO_TOKEN : str = os.getenv("TURBO_TOKEN") or ""

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
            conn = libsql.connect(database=TURBO_URL, auth_token=TURBO_TOKEN)
            cursor = conn.cursor()
            cursor.execute("SELECT invited_members FROM invites WHERE user_id = ? AND guild_id = ?", (inviter.id, member.guild.id))
            result = cursor.fetchone()

            if result:
                invited_members = json.loads(result[0]) 
                if str(member.id) in invited_members:
                    await welcome_channel.send(f"{inviter.mention}, vous avez déjà invité {member.mention} !")
                    conn.close()
                    return

            if result:
                invited_members.append(str(member.id))
            else:
                invited_members = [str(member.id)]

            cursor.execute("INSERT OR REPLACE INTO invites (user_id, guild_id, last_invite_time, invited_members) VALUES (?, ?, ?, ?)",
                           (inviter.id, member.guild.id, time.time(), json.dumps(invited_members)))
            conn.commit()
            conn.close()

            await welcome_channel.send(
                f"Bienvenue {member.mention} ! (Invité par {inviter.mention} qui a invité : {invites_count} membres)."
            )
        else:
            await welcome_channel.send(f"Bienvenue {member.mention} !\nJe n'ai pas pu identifier l'inviteur.")

    @commands.hybrid_command()
    async def invited(self, ctx, member: discord.Member):
        """Donne la liste des membres invités par un membre."""
        conn = libsql.connect(database=TURBO_URL, auth_token=TURBO_TOKEN)
        cursor = conn.cursor()

        cursor.execute("SELECT invited_members FROM invites WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
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

        conn.close()

async def setup(bot):
    await bot.add_cog(Welcome(bot))
