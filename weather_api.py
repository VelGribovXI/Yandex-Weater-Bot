import aiohttp
from typing import Optional, Dict

class WeatherService:
    """Сервис для работы с API погоды"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Используем OpenWeatherMap API (бесплатно)
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather(self, city: str) -> Optional[Dict]:
        """
        Получает погоду для города
        Возвращает None если город не найден
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',  # Цельсии
            'lang': 'ru'        # Русский язык
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._format_weather(data)
                    elif resp.status == 404:
                        return None  # Город не найден
                    else:
                        return None  # Другая ошибка
            except aiohttp.ClientError:
                return None  # Ошибка сети
    
    def _format_weather(self, data: Dict) -> Dict:
        """Форматирует ответ API в удобный вид"""
        return {
            'city': data['name'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'].capitalize()
        }
    
    def make_weather_message(self, weather: Dict) -> str:
        """Создает красивое сообщение с погодой"""
        return (
            f"🌍 *{weather['city']}*\n\n"
            f"🌡️ Температура: *{weather['temperature']}°C*\n"
            f"🤔 Ощущается как: *{weather['feels_like']}°C*\n"
            f"💧 Влажность: *{weather['humidity']}%*\n"
            f"💨 Ветер: *{weather['wind_speed']} м/с*\n"
            f"📝 {weather['description']}\n\n"
            f"#Погода #{weather['city'].lower()}"
        )
