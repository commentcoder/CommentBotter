import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
token : str = os.getenv("DISCORD_TOKEN") or ""

class CommentBotter(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                extension = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    print(f"Loaded extension: {extension}")
                except Exception as e:
                    print(f"Failed to load extension {extension}: {e}")
    
        await self.tree.sync()
        print("Les commandes slash ont été synchronisées.")

intents = discord.Intents.all()
bot = CommentBotter(command_prefix='!', intents=intents)

if __name__ == "__main__":
    keep_alive()

    bot.run(token=token)