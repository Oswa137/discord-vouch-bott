

import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

guild_id = 1365186060581077012  # Cambia esto por el ID de tu servidor para registrar el comando rápidamente

class VouchModal(discord.ui.Modal, title="Vouch Form"):
    usuario = discord.ui.TextInput(label="Menciona al usuario (@usuario)", placeholder="@usuario", required=True)
    estrellas = discord.ui.TextInput(label="Estrellas (1-5)", placeholder="Pon un número del 1 al 5", required=True)
    experiencia = discord.ui.TextInput(label="Describe tu experiencia", style=discord.TextStyle.paragraph, placeholder="Escribe tu experiencia aquí", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user_mention = self.usuario.value
        stars = self.estrellas.value
        experience = self.experiencia.value

        # Convertir a emojis de estrellas
        try:
            stars_int = int(stars)
            if stars_int < 1 or stars_int > 5:
                raise ValueError
            star_emojis = "⭐" * stars_int
        except ValueError:
            await interaction.response.send_message("Número de estrellas inválido. Debe ser un número entre 1 y 5.", ephemeral=True)
            return

        embed = discord.Embed(title="📜 Nuevo Vouch", color=0x00ff00)
        embed.add_field(name="👤 Usuario Voucheado", value=user_mention, inline=False)
        embed.add_field(name="⭐ Calificación", value=star_emojis, inline=False)
        embed.add_field(name="📝 Experiencia", value=experience, inline=False)
        embed.set_footer(text=f"Vouch por {interaction.user.display_name}")

        await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=guild_id))
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(e)
    print(f"Bot listo como {bot.user}")

@bot.tree.command(name="vouch", description="Envía un vouch a un usuario.", guild=discord.Object(id=guild_id))
async def vouch(interaction: discord.Interaction):
    await interaction.response.send_modal(VouchModal())

# Para Replit:
token = os.environ["TOKEN"]  # Guarda tu token en el Secret Manager de Replit con el nombre TOKEN
bot.run(token)
Add bot main file
