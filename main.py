import discord
from discord.ext import commands
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# 🌐 WEB SERVER (RENDER FIX)
# =========================
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# =========================
# 🤖 BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


# =========================
# 📦 LOAD COGS
# =========================
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def setup_hook():
    await load_cogs()


# =========================
# 🚀 START WEB + BOT
# =========================
threading.Thread(target=run_web).start()

bot.run(os.environ["TOKEN"])
