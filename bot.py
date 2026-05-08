import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from weather_api import WeatherService
from cache import WeatherCache

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class WeatherBot:
    def __init__(self, token: str, weather_api_key: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.weather_service = WeatherService(weather_api_key)
        self.cache = WeatherCache()
        
        # Регистрируем обработчики команд
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрация всех команд бота"""
        
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            await message.answer(
                "🌤️ *Привет! Я бот погоды!*\n\n"
                "Просто напиши название города,\n"
                "и я расскажу о погоде.\n\n"
                "Пример: *Москва* или *London*",
                parse_mode="Markdown"
            )
        
        @self.dp.message(Command("help"))
        async def cmd_help(message: types.Message):
            await message.answer(
                "📖 *Как пользоваться:*\n"
                "1. Напиши название города\n"
                "2. Получи погоду\n\n"
                "🔧 *Доступные команды:*\n"
                "/start - Приветствие\n"
                "/help - Эта справка\n\n"
                "💡 *Совет:* Можно писать на русском или английском",
                parse_mode="Markdown"
            )
        
        @self.dp.message()
        async def handle_weather(message: types.Message):
            city = message.text.strip()
            
            # Отправляем "печатает" для имитации работы
            await message.bot.send_chat_action(
                chat_id=message.chat.id,
                action="typing"
            )
            
            # Проверяем кэш
            cached_weather = self.cache.get(city.lower())
            if cached_weather:
                await message.answer(
                    self.weather_service.make_weather_message(cached_weather),
                    parse_mode="Markdown"
                )
                return
            
            # Идем в API
            weather = await self.weather_service.get_weather(city)
            
            if weather:
                # Сохраняем в кэш
                self.cache.set(city.lower(), weather)
                
                # Отправляем результат
                await message.answer(
                    self.weather_service.make_weather_message(weather),
                    parse_mode="Markdown"
                )
            else:
                await message.answer(
                    f"❌ Город *{city}* не найден!\n"
                    "Проверьте название и попробуйте снова.",
                    parse_mode="Markdown"
                )
    
    async def start(self):
        """Запуск бота"""
        logging.info("Бот запущен!")
        await self.dp.start_polling(self.bot)
