@echo off
chcp 65001 >nul
cd /d "%~dp0"

title ZoVych - Discord bot
echo Запуск бота... Окно не закрывайте. Для остановки: Ctrl+C
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [Ошибка] Не найден .venv. Сначала установите зависимости:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist ".env" (
    echo [Ошибка] Нет файла .env. Скопируйте .env.example в .env и укажите DISCORD_TOKEN.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" bot.py
echo.
echo Бот остановлен.
pause
