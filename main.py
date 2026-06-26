import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


# =========================
# CARGAR COGS
# =========================
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def setup_hook():
    await load_cogs()


# =========================
# TOKEN DESDE RENDER
# =========================
bot.run(os.environ["TOKEN"])
