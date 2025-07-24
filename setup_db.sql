-- Скрипт для настройки базы данных на удаленном PostgreSQL сервере
-- Выполните этот скрипт на вашем сервере PostgreSQL

-- Создание таблицы для логирования действий бота
CREATE TABLE IF NOT EXISTS bot_actions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    action_description TEXT,
    message_text TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_bot_actions_user_id ON bot_actions(user_id);
CREATE INDEX IF NOT EXISTS idx_bot_actions_chat_id ON bot_actions(chat_id);
CREATE INDEX IF NOT EXISTS idx_bot_actions_action_type ON bot_actions(action_type);

-- Комментарии к таблице и колонкам
COMMENT ON TABLE bot_actions IS 'Таблица для логирования действий бота';
COMMENT ON COLUMN bot_actions.id IS 'Уникальный идентификатор';
COMMENT ON COLUMN bot_actions.user_id IS 'Telegram ID пользователя';
COMMENT ON COLUMN bot_actions.chat_id IS 'Telegram ID чата';
COMMENT ON COLUMN bot_actions.action_type IS 'Тип действия (модерация, команда и т.д.)';
COMMENT ON COLUMN bot_actions.action_description IS 'Описание действия';
COMMENT ON COLUMN bot_actions.message_text IS 'Текст сообщения';
COMMENT ON COLUMN bot_actions.timestamp IS 'Время выполнения действия';
COMMENT ON COLUMN bot_actions.created_at IS 'Время создания записи';

-- Проверка успешного создания таблицы
SELECT 'Таблица bot_actions успешно создана!' as result;

-- Показать структуру таблицы
-- \d+ bot_actions
