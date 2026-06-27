import os
import discord
from discord import app_commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

import config


# =========================
# 🌐 KEEP ALIVE (Render)
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
# BOT
# =========================
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands sincronizados")


client = MyClient()


# =========================
# READY
# =========================
@client.event
async def on_ready():
    print(f"🔥 Bot conectado como {client.user}")


# =========================
# 💡 SUGERENCIA
# =========================
@client.tree.command(name="suggest", description="Enviar una sugerencia")
async def suggest(interaction: discord.Interaction, idea: str):

    channel = interaction.guild.get_channel(config.SUGGEST_CHANNEL_ID)

    if not channel:
        return await interaction.response.send_message("❌ Canal no encontrado", ephemeral=True)

    embed = discord.Embed(
        title="💡 Nueva sugerencia",
        description=idea,
        color=0x00B0FF
    )
    embed.set_footer(text=f"Propuesto por {interaction.user}")

    msg = await channel.send(embed=embed)

    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

    await interaction.response.send_message("✅ Sugerencia enviada", ephemeral=True)


# =========================
# 🔧 FUNCIÓN BASE
# =========================
async def move_suggestion(interaction, message_id: int, channel_id: int, title: str, color: int):

    suggest_channel = interaction.guild.get_channel(config.SUGGEST_CHANNEL_ID)
    target_channel = interaction.guild.get_channel(channel_id)

    if not suggest_channel or not target_channel:
        return await interaction.response.send_message("❌ Canales no configurados", ephemeral=True)

    try:
        msg = await suggest_channel.fetch_message(message_id)
    except:
        return await interaction.response.send_message("❌ Mensaje no encontrado", ephemeral=True)

    if not msg.embeds:
        return await interaction.response.send_message("❌ El mensaje no tiene embed", ephemeral=True)

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

    await interaction.response.send_message("✅ Acción realizada", ephemeral=True)


# =========================
# ✅ ACCEPT
# =========================
@client.tree.command(name="accept", description="Aceptar sugerencia")
async def accept(interaction: discord.Interaction, message_id: str):

    await move_suggestion(
        interaction,
        int(message_id),
        config.APPROVED_CHANNEL_ID,
        "📌 Sugerencia aprobada",
        0x2ECC71
    )


# =========================
# ❌ DENY
# =========================
@client.tree.command(name="deny", description="Rechazar sugerencia")
async def deny(interaction: discord.Interaction, message_id: str):

    await move_suggestion(
        interaction,
        int(message_id),
        config.DENIED_CHANNEL_ID,
        "❌ Sugerencia rechazada",
        0xE74C3C
    )


# =========================
# START
# =========================
client.run(os.getenv("TOKEN"))
