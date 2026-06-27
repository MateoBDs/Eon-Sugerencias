import discord
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = TU_ID_DEL_SERVIDOR

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        try:
            await self.tree.sync(guild=guild)
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)

            print("🧨 comandos borrados correctamente")

        except Exception as e:
            print("ERROR:", e)

        await self.close()

client = Client()
client.run(TOKEN)
