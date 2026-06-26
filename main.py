import os
import discord
import asyncio
from discord.ext import commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

import config

# =========================
# 🌐 KEEP ALIVE (igual que tu bot bueno)
# =========================
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot activo")

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

Thread(target=run_web, daemon=True).start()

# =========================
# 🤖 BOT
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


# =========================
# 💡 SUGERENCIA
# =========================
@bot.command()
async def suggest(ctx, *, idea: str):

    channel = ctx.guild.get_channel(config.SUGGEST_CHANNEL_ID)

    if not channel:
        return await ctx.send("❌ Canal de sugerencias no encontrado.")

    embed = discord.Embed(
        title="💡 Nueva sugerencia",
        description=idea,
        color=0x00b0ff
    )
    embed.set_footer(text=f"Propuesto por {ctx.author}")

    msg = await channel.send(embed=embed)

    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

    await ctx.send("✅ Sugerencia enviada.")


# =========================
# ✅ ACEPTAR
# =========================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def accept(ctx, message_id: int):

    await move_suggestion(
        ctx,
        message_id,
        config.APPROVED_CHANNEL_ID,
        "📌 Sugerencia aprobada",
        0x2ecc71
    )


# =========================
# ❌ RECHAZAR
# =========================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def deny(ctx, message_id: int):

    await move_suggestion(
        ctx,
        message_id,
        config.DENIED_CHANNEL_ID,
        "❌ Sugerencia rechazada",
        0xe74c3c
    )


# =========================
# 🔧 FUNCIÓN INTERNA
# =========================
async def move_suggestion(ctx, message_id, channel_id, title, color):

    suggest_channel = ctx.guild.get_channel(config.SUGGEST_CHANNEL_ID)
    target_channel = ctx.guild.get_channel(channel_id)

    if not suggest_channel or not target_channel:
        return await ctx.send("❌ Canales no configurados.")

    try:
        msg = await suggest_channel.fetch_message(message_id)
    except:
        return await ctx.send("❌ Mensaje no encontrado.")

    if not msg.embeds:
        return await ctx.send("❌ El mensaje no tiene embed.")

    embed = msg.embeds[0]

    new_embed = discord.Embed(
        title=title,
        description=embed.description,
        color=color
    )

    if embed.footer:
        new_embed.set_footer(text=embed.footer.text)

    await target_channel.send(embed=new_embed)
    await msg.delete()

    await ctx.send("✅ Sugerencia movida correctamente.")


# =========================
# 🚀 START
# =========================
bot.run(os.getenv("TOKEN"))
