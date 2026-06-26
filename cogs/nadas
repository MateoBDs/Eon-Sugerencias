import discord
from discord.ext import commands
import config


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # =========================
    # 💡 CREAR SUGERENCIA
    # =========================
    @commands.command()
    async def suggest(self, ctx, *, idea: str):

        channel = ctx.guild.get_channel(config.SUGGEST_CHANNEL_ID)

        if not channel:
            return await ctx.send("❌ No existe el canal de sugerencias.")

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
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def accept(self, ctx, message_id: int):
        await self.move(
            ctx,
            message_id,
            config.APPROVED_CHANNEL_ID,
            "📌 Sugerencia aprobada",
            0x2ecc71
        )


    # =========================
    # ❌ RECHAZAR
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def deny(self, ctx, message_id: int):
        await self.move(
            ctx,
            message_id,
            config.DENIED_CHANNEL_ID,
            "❌ Sugerencia rechazada",
            0xe74c3c
        )


    # =========================
    # 🔧 FUNCIÓN INTERNA
    # =========================
    async def move(self, ctx, message_id, channel_id, title, color):

        channel = ctx.guild.get_channel(config.SUGGEST_CHANNEL_ID)
        target = ctx.guild.get_channel(channel_id)

        if not channel or not target:
            return await ctx.send("❌ Faltan canales configurados.")

        try:
            msg = await channel.fetch_message(message_id)
        except:
            return await ctx.send("❌ No se encontró la sugerencia.")

        if not msg.embeds:
            return await ctx.send("❌ Ese mensaje no tiene embed.")

        embed = msg.embeds[0]

        new_embed = discord.Embed(
            title=title,
            description=embed.description,
            color=color
        )

        if embed.footer:
            new_embed.set_footer(text=embed.footer.text)

        await target.send(embed=new_embed)
        await msg.delete()

        await ctx.send("✅ Sugerencia movida correctamente.")


async def setup(bot):
    await bot.add_cog(Suggestions(bot))
