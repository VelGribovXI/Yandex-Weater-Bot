from datetime import datetime, timedelta
from typing import Dict, Optional

class WeatherCache:
    """Простой кэш для хранения погоды на 10 минут"""
    
    def __init__(self, ttl_minutes: int = 10):
        self.cache: Dict[str, tuple] = {}  # city -> (weather_data, timestamp)
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, city: str) -> Optional[Dict]:
        """Получить погоду из кэша если она еще актуальна"""
        if city in self.cache:
            weather, timestamp = self.cache[city]
            if datetime.now() - timestamp < self.ttl:
                return weather
            else:
                del self.cache[city]
        return None
    
    def set(self, city: str, weather: Dict):
        """Сохранить погоду в кэш"""
        self.cache[city] = (weather, datetime.now())
