"""
Discord-бот: ставит реакцию 🇿 на каждое новое сообщение
на указанном сервере (GUILD_ID).
"""

import os
import logging

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = (os.getenv("GUILD_ID") or "").strip()

if not TOKEN:
    raise SystemExit("Укажите DISCORD_TOKEN в файле .env")

TARGET_GUILD_ID = None
if GUILD_ID:
    try:
        TARGET_GUILD_ID = int(GUILD_ID)
    except ValueError:
        raise SystemExit("GUILD_ID должен быть числом")

# regional_indicator_z / o / v  →  ZOV
REACTIONS = ("🇿", "🇴", "🇻")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("z-bot")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    if TARGET_GUILD_ID is None:
        names = ", ".join(g.name for g in client.guilds) or "(нет серверов)"
        log.info("Бот онлайн как %s | все серверы: %s", client.user, names)
        return

    guild = client.get_guild(TARGET_GUILD_ID)
    if guild is None:
        log.warning(
            "Бот онлайн как %s, но сервер %s не найден. "
            "Проверьте GUILD_ID и что бот добавлен на сервер.",
            client.user,
            TARGET_GUILD_ID,
        )
    else:
        log.info("Бот онлайн как %s | сервер: %s", client.user, guild.name)


@client.event
async def on_message(message: discord.Message):
    # Игнорируем ЛС
    if message.guild is None:
        return

    # Если указан GUILD_ID — только этот сервер
    if TARGET_GUILD_ID is not None and message.guild.id != TARGET_GUILD_ID:
        return

    # Не реагируем на свои сообщения (избегаем лишних запросов к API)
    if message.author.id == client.user.id:
        return

    for emoji in REACTIONS:
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException as exc:
            # Нет прав, сообщение удалено, rate limit и т.п.
            log.warning(
                "Не удалось поставить %s в #%s: %s",
                emoji,
                getattr(message.channel, "name", message.channel.id),
                exc,
            )
            break


if __name__ == "__main__":
    client.run(TOKEN)
