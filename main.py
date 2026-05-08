import os
from dotenv import load_dotenv
from bot import WeatherBot

# Загружаем переменные окружения
load_dotenv()

def main():
    # Получаем ключи из .env
    bot_token = os.getenv("BOT_TOKEN")
    weather_api_key = os.getenv("WEATHER_API_KEY")
    
    # Проверяем что ключи есть
    if not bot_token or not weather_api_key:
        print("❌ Ошибка: Не найдены ключи в файле .env")
        print("Создайте файл .env с переменными:")
        print("BOT_TOKEN=ваш_токен")
        print("WEATHER_API_KEY=ваш_ключ")
        return
    
    # Создаем и запускаем бота
    bot = WeatherBot(bot_token, weather_api_key)
    
    try:
        import asyncio
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")

if __name__ == "__main__":
    main()
