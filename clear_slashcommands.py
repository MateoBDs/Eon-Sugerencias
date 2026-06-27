import os
import discord
import asyncio

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"🔥 Conectado como {client.user}")

    guild = discord.Object(id=GUILD_ID)

    try:
        # 🔥 BORRAR comandos del servidor
        tree.clear_commands(guild=guild)
        await tree.sync(guild=guild)

        print("🧨 Slash commands eliminados correctamente")

    except Exception as e:
        print("❌ Error:", e)

    await client.close()


client.run(TOKEN)
