import os
import asyncpg
import logging
from datetime import datetime

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

logger = logging.getLogger(__name__)

pool = None  # Глобальный пул

async def init_pool():
    global pool
    if pool is None:
        try:
            pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                min_size=1,
                max_size=5
            )
            logger.info(f"Установлено соединение с базой данных {DB_NAME} на {DB_HOST}:{DB_PORT} (пользователь: {DB_USER})")
        except Exception as e:
            logger.error(f"Ошибка при подключении к базе данных: {e}")
            raise

async def log_action(user_id: int, chat_id: int, action_type: str, action_description: str = None, message_text: str = None):
    if pool is None:
        await init_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            '''INSERT INTO bot_actions 
               (user_id, chat_id, action_type, action_description, message_text, timestamp) 
               VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)''',
            user_id, chat_id, action_type, action_description, message_text
        )

async def get_chat_stats(chat_id: int):
    """Получить статистику для конкретного чата"""
    if pool is None:
        await init_pool()
    async with pool.acquire() as conn:
        # Общее количество действий
        total_actions = await conn.fetchval(
            'SELECT COUNT(*) FROM bot_actions WHERE chat_id = $1',
            chat_id
        )
        
        # Количество удалённых сообщений
        deleted_messages = await conn.fetchval(
            'SELECT COUNT(*) FROM bot_actions WHERE chat_id = $1 AND action_type = $2',
            chat_id, 'profanity_filter'
        )
        
        # Количество уникальных пользователей
        unique_users = await conn.fetchval(
            'SELECT COUNT(DISTINCT user_id) FROM bot_actions WHERE chat_id = $1',
            chat_id
        )
        
        return {
            'total_actions': total_actions or 0,
            'deleted_messages': deleted_messages or 0,
            'unique_users': unique_users or 0
        }

async def create_table():
    if pool is None:
        await init_pool()
    try:
        async with pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS bot_actions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    chat_id BIGINT NOT NULL,
                    action_type VARCHAR(50) NOT NULL,
                    action_description TEXT,
                    message_text TEXT,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Создание индексов для оптимизации запросов
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_bot_actions_user_id ON bot_actions(user_id)')
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_bot_actions_chat_id ON bot_actions(chat_id)')
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_bot_actions_action_type ON bot_actions(action_type)')
            
        logger.info("Таблица bot_actions проверена/создана в базе данных с новой структурой.")
    except Exception as e:
        logger.error(f"Ошибка при создании/проверке таблицы bot_actions: {e}")
        raise
