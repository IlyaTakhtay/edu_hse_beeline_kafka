import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # ClickHouse
        self.CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
        self.CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT', 9000))
        self.CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
        self.CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
        self.CLICKHOUSE_DB = os.getenv('CLICKHOUSE_DB', 'default')

        # PostgreSQL
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
        self.POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
        self.POSTGRES_DB = os.getenv('POSTGRES_DB', 'app_analytics')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', 'app_user')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'app_password')
        self.POSTGRES_SCHEMA = os.getenv('POSTGRES_SCHEMA', 'public')

        # Параметры генерации
        # Размер батча: если указан BATCH_SIZE, используем его как фиксированный,
        # иначе используем диапазон BATCH_SIZE_MIN - BATCH_SIZE_MAX.
        batch_size_env = os.getenv('BATCH_SIZE')
        if batch_size_env is not None and batch_size_env.strip() != '':
            self.BATCH_SIZE_FIXED = int(batch_size_env)
            self.BATCH_IS_RANDOM = False
        else:
            self.BATCH_SIZE_MIN = int(os.getenv('BATCH_SIZE_MIN', 5))
            self.BATCH_SIZE_MAX = int(os.getenv('BATCH_SIZE_MAX', 15))
            self.BATCH_IS_RANDOM = True

        # Интервал
        sleep_env = os.getenv('SLEEP_SECONDS')
        if sleep_env is not None and sleep_env.strip() != '':
            self.SLEEP_FIXED = float(sleep_env)
            self.SLEEP_IS_RANDOM = False
        else:
            self.SLEEP_MIN = float(os.getenv('SLEEP_MIN', 0.1))
            self.SLEEP_MAX = float(os.getenv('SLEEP_MAX', 0.5))
            self.SLEEP_IS_RANDOM = True

        # Вероятности
        self.CLICK_PROBABILITY = float(os.getenv('CLICK_PROBABILITY', 0.2))
        self.INSTALL_PROBABILITY = float(os.getenv('INSTALL_PROBABILITY', 0.4))
        self.ORGANIC_PROBABILITY = float(os.getenv('ORGANIC_PROBABILITY', 0.1))

        self.BANNER_COUNT = int(os.getenv('BANNER_COUNT', 5))
        self.CAMPAIGN_COUNT = int(os.getenv('CAMPAIGN_COUNT', 3))

        # Константы
        self.PLACEMENTS = ['site', 'app', 'social']
        self.DEVICE_TYPES = ['phone', 'tablet', 'desktop']
        self.OS_LIST = ['ios', 'android', 'windows', 'linux']
        self.CITIES = [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург',
            'Казань', 'Нижний Новгород', 'Челябинск', 'Самара', 'Омск',
            'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Воронеж', 'Пермь', 'Волгоград'
        ]
        self.ACTION_TYPES = ['registration', 'first_order', 'tariff_switch']
