# Тут будуть знаходитись / команди
import os

import aiohttp
import discord
import random
from discord.ext import commands
from discord import app_commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Декоратор, який перетворює метод на слеш-команду
    @app_commands.command(name="виклик", description="Викликає обраного користувача до войсу")
    async def viklik(self, interaction: discord.Interaction, member: discord.Member):
        SPECIAL_ID = 323 #621295677875552257
        if member.id == SPECIAL_ID:
            await member.send(f"Оцей хуєсос -> {interaction.user.mention} на тебе спам хотів кинути!")
            await interaction.response.send_message("А хуй тобі, йому не можна спамити!!!")
        else:
            await interaction.response.send_message("Зараз покличемо!")
            i = 0
            while i < 20:
                await member.send(f"Тебе хуєсоса кличе у войс ця людина -> {interaction.user.mention}")
                i += 1

    @app_commands.command(name="гей", description="Показує на скільки відсотків людина є геєм")
    async def gei(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{member.mention} гей на {random.randint(1, 100) }%")

    @app_commands.command(name="ai", description="Відправляє повідомлення до геміні")
    async def ask_gemini(self, interaction: discord.Interaction, prompt: str):
        # 1. Відразу кажемо Discord: "Бот прийняв команду і думає..."
        # В інтерфейсі користувача з'явиться напис "Бот думає..."
        await interaction.response.defer()

        try:
            api_key = os.getenv("GEMINI_KEY")
            if not api_key:
                # Оскільки ми використали defer(), відповідати тепер треба через followup
                await interaction.followup.send("Помилка: Ключ GEMINI_KEY не знайдено!")
                return

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
            frazochki = ["Нет, іді нахуй", "Хуесос ебаний", "Я твою маму вертел", "Пішов нахуй", "Я твій рот єбав"]

            system_style = (
                "Ти знаходишся на сервері, відповідай так само як до тебе. Якщо в повідомленні є мат, "
                "можеш також використати, АЛЕ МАТ НЕ Є ОБОВ'ЯЗКОВИМ. Якщо мату в повідомленні немає мату можеш використати мат з шансом 1/5. "
                f"Відповідай виключно українською. {frazochki} "
                "Можеш використовувати ці фрази для генерації відповідей, якщо в повідомленні був мат"
            )

            json_body = {
                "system_instruction": {
                    "parts": [{"text": system_style}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json_body) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Gemini Помилка {response.status}: {error_text}")
                        await interaction.followup.send(f"Помилка API! Код: {response.status}")
                        return

                    response_json = await response.json()
                    answer = response_json["candidates"][0]["content"]["parts"][0]["text"]

                    # 2. Відправляємо згенерований текст користувачу
                    # followup.send автоматично замінить напис "Бот думає..." на цю відповідь
                    await interaction.followup.send(answer)

        except Exception as e:
            print(f"Виникла помилка: {e}")
            await interaction.followup.send("Виникла технічна помилка під час обробки запиту.")

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json_body) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Gemini Помилка {response.status}: {error_text}")
                        return f"Помилка Application Programming Interface! Код: {response.status}. Глянь логи!"

                    response_json = await response.json()

                    return response_json["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print(f"Виникла помилка: {e}")
            return " "

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))