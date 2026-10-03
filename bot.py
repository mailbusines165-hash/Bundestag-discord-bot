import os
from io import BytesIO
from datetime import datetime

import discord
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
ALLOWED_CHANNEL_ID = os.getenv("ALLOWED_CHANNEL_ID")
ALLOWED_ROLE_ID = os.getenv("ALLOWED_ROLE_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in den Umgebungsvariablen.")

def env_int(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None

GUILD_ID = env_int(GUILD_ID)
ALLOWED_CHANNEL_ID = env_int(ALLOWED_CHANNEL_ID)
ALLOWED_ROLE_ID = env_int(ALLOWED_ROLE_ID)

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

def get_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def make_voucher(amount, user):
    width, height = 1400, 800
    img = Image.new("RGB", (width, height), "#f4f1e8")
    draw = ImageDraw.Draw(img)

    # Decorative border
    draw.rounded_rectangle((35, 35, width-35, height-35), radius=30,
                           outline="#333333", width=5)
    draw.rounded_rectangle((60, 60, width-60, height-60), radius=22,
                           outline="#777777", width=2)

    title_font = get_font(58, True)
    subtitle_font = get_font(34, False)
    amount_font = get_font(92, True)
    normal_font = get_font(30, False)
    small_font = get_font(25, False)

    draw.text((width/2, 120), "LANDTAG / BUNDESTAG", font=title_font,
              anchor="mm", fill="#222222")
    draw.text((width/2, 185), "AUSZAHLUNG", font=subtitle_font,
              anchor="mm", fill="#333333")

    draw.line((180, 235, width-180, 235), fill="#777777", width=2)

    amount_text = f"{amount:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    draw.text((width/2, 350), amount_text, font=amount_font,
              anchor="mm", fill="#111111")

    draw.text((150, 505), f"Auszahlung von: {user}", font=normal_font,
              fill="#222222")
    draw.text((150, 555),
              f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
              font=normal_font, fill="#222222")

    # Prominent safety label
    draw.rounded_rectangle((150, 625, width-150, 715), radius=18,
                           outline="#8b0000", width=3)
    draw.text((width/2, 670),
              "SIMULATION – NICHT AMTLICH / KEIN ZAHLUNGSBELEG",
              font=small_font, anchor="mm", fill="#8b0000")

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

@bot.event
async def on_ready():
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        await tree.sync(guild=guild)
        print(f"Slash-Commands für Guild {GUILD_ID} synchronisiert.")
    else:
        await tree.sync()
        print("Globale Slash-Commands synchronisiert.")
    print(f"Eingeloggt als {bot.user}")

def allowed(interaction: discord.Interaction):
    if ALLOWED_CHANNEL_ID and interaction.channel_id != ALLOWED_CHANNEL_ID:
        return False
    if ALLOWED_ROLE_ID:
        member = interaction.user
        if isinstance(member, discord.Member):
            return any(role.id == ALLOWED_ROLE_ID for role in member.roles)
        return False
    return True

@tree.command(name="auszahlung", description="Erstellt eine Auszahlungskarte als Simulation.")
@app_commands.describe(betrag="Betrag in Euro, z.B. 2500.00")
async def auszahlung(interaction: discord.Interaction, betrag: app_commands.Range[float, 0.01, 1000000.0]):
    if not allowed(interaction):
        await interaction.response.send_message(
            "Dieser Befehl ist in diesem Channel bzw. für diese Rolle nicht freigegeben.",
            ephemeral=True
        )
        return

    # User name is taken from Discord automatically.
    user_name = interaction.user.display_name
    image = make_voucher(float(betrag), user_name)
    file = discord.File(image, filename="auszahlung_simulation.png")

    await interaction.response.send_message(
        "Hier ist die Auszahlungskarte als Simulation:",
        file=file
    )

@tree.command(name="ping", description="Prüft, ob der Bot online ist.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓", ephemeral=True)

@tree.command(name="hilfe", description="Zeigt die verfügbaren Befehle.")
async def hilfe(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Verfügbare Befehle**\n"
        "`/auszahlung betrag:` – erstellt eine Auszahlungskarte (Simulation)\n"
        "`/ping` – prüft den Bot\n"
        "`/hilfe` – zeigt diese Hilfe",
        ephemeral=True
    )

bot.run(TOKEN)
