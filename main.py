import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
DEBUG_CHANNEL_ID = int(os.getenv("DEBUG_CHANNEL_ID"))
FORUM_AIDE_CHANNEL_ID = int(os.getenv("FORUM_AIDE_CHANNEL_ID"))
PRESENTATIONS_CHANNEL_ID = int(os.getenv("PRESENTATIONS_CHANNEL_ID"))


@bot.event
async def on_member_join(member: discord.Member):
  welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID) 

  forum_aide_channel = bot.get_channel(FORUM_AIDE_CHANNEL_ID)
  presentations_channel = bot.get_channel(PRESENTATIONS_CHANNEL_ID)

  await welcome_channel.send(f"Bienvenue {member.mention} ! N'hésite pas à te découvrir le forum pour poser tes questions {forum_aide_channel.mention}. Et tu peux aussi te présenter quand tu te sens à l'aise (si tu veux) dans {presentations_channel.mention}.")


if __name__ == "__main__":
  keep_alive()
  bot.run(token=token)
