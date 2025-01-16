import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
token : str = os.getenv("DISCORD_TOKEN") or ""

class CommentBotter(commands.Bot):
  async def setup_hook(self):
    for extension in ['database']:
      await self.load_extension(f'cogs.{extension}')
    
    await self.tree.sync()
    print("Les commandes slash ont été synchronisées.")

intents = discord.Intents.all()
bot = CommentBotter(command_prefix='!', intents=intents)

if __name__ == "__main__":
    keep_alive()

    bot.run(token=token)