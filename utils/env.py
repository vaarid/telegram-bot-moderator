import os
from dotenv import load_dotenv


def load_env(env_file: str = None):
    """
    Загружает переменные окружения из указанного файла или из .env по умолчанию.
    """
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    # Проверка обязательных переменных
    required_vars = [
        'BOT_TOKEN', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Не найдена обязательная переменная окружения: {var}") 