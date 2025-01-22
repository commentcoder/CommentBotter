import discord
from discord.ext import commands

MESSAGES = {
    "origin": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "why": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "how": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "what": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "who": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "udemy": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    },
    "age": {
        "message_id": 0,
        "reaction": [1, 2, 3]
    }
}

class RoleAssigner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Écoute les réactions ajoutées."""
        if payload.message_id != self.message_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_mapping = {
            "✅": 123456789012345678,
            "❌": 987654321098765432
        }

        role_id = role_mapping.get(payload.emoji.name)
        if role_id is None:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is not None:
            await member.add_roles(role)
            print(f"Ajouté le rôle {role.name} à {member.display_name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Écoute les réactions supprimées."""
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_mapping = {
            "✅": 123456789012345678,
            "❌": 987654321098765432
        }

        role_id = role_mapping.get(payload.emoji.name)
        if role_id is None:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is not None:
            await member.remove_roles(role)
            print(f"Retiré le rôle {role.name} de {member.display_name}")

    @commands.command(name="setrolemessage")
    @commands.has_permissions(administrator=True)
    async def set_role_message(self, ctx, message_id: int):
        """Définit l'ID du message à surveiller pour les réactions."""
        self.message_id = message_id
        await ctx.send(f"L'ID du message de rôle a été défini sur {message_id}")

async def setup(bot):
    await bot.add_cog(RoleAssigner(bot))
