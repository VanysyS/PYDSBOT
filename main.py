import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
# Ця функція автоматично викликається перед тим, як бот підключиться до серверів
@bot.event
async def setup_hook():
    # Завантаження модуля з кірньової теки
    await bot.load_extension("Cogs.commands")
    # Відправляємо наші slash-команди на сервери Discord
    await bot.tree.sync()


@bot.event
async def on_ready():
    print(f'Бот {bot.user} в мережі та готовий до роботи!')

# Запускає бота. В лапках токен
token = os.getenv("DISCORD_TOKEN")
bot.run(token)