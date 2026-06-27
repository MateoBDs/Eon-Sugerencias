import discord
import asyncio
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 123456789012345678  # tu servidor

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        # 🔥 BORRA comandos del servidor
        self.tree.clear_commands(guild=guild)
        await self.tree.sync(guild=guild)

        print("🧨 Comandos borrados en guild")
        await self.close()

client = Client()
client.run(TOKEN)
