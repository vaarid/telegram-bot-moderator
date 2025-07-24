# 🤖 Telegram Bot Moderator

Полнофункциональный Telegram-бот для модерации чатов с автоматическим удалением нецензурной лексики, логированием действий и статистикой.

## 🚀 Функциональность

### Основные возможности:
- **Автоматическое удаление сообщений** с нецензурной лексикой
- **Предупреждения пользователям** при нарушении правил
- **Логирование всех действий** в PostgreSQL базу данных
- **Статистика чата** для администраторов
- **Команды управления** (`/start`, `/help`, `/rules`, `/stats`)
- **Интерактивные кнопки** для быстрого доступа к правилам

### Модерация:
- Фильтрация нецензурной лексики на русском языке
- Настраиваемый список запрещённых слов
- Автоматическое удаление нарушающих сообщений
- Отправка предупреждений нарушителям

### Логирование:
- Все действия бота записываются в БД
- Отслеживание пользователей и их действий
- Статистика по чатам и пользователям
- История модерации

## 🛠 Технологии

- **Python 3.10+**
- **aiogram 3.x** - Telegram Bot API
- **PostgreSQL** - база данных
- **Docker & Docker Compose** - контейнеризация
- **asyncpg** - асинхронное подключение к БД

## 📋 Требования

- Docker и Docker Compose
- PostgreSQL сервер (локальный или удалённый)
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/vaarid/telegram-bot-moderator.git
cd telegram-bot-moderator
```

### 2. Настройка переменных окружения
Скопируйте `EnvExample` в `.env` и заполните параметры:
```bash
cp EnvExample .env
```

Отредактируйте `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### 3. Запуск через Docker
```bash
# Сборка и запуск
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

### 4. Настройка бота в Telegram
1. Добавьте бота в группу
2. Сделайте бота администратором
3. Включите право "Удаление сообщений"
4. Отключите Privacy Mode через [@BotFather](https://t.me/BotFather)

## 📖 Команды бота

| Команда | Описание | Доступ |
|---------|----------|--------|
| `/start` | Приветствие и описание бота | Все |
| `/help` | Справка по использованию | Все |
| `/rules` | Правила чата | Все |
| `/stats` | Статистика чата | Только админы |

## 🗄 Структура базы данных

### Таблица `bot_actions`
```sql
CREATE TABLE bot_actions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    action_description TEXT,
    message_text TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Типы действий:
- `profanity_filter` - удаление сообщений с матом
- `command` - выполнение команд
- `callback` - нажатие кнопок
- `bot_added` - добавление бота в чат

## 📁 Структура проекта

```
telegram-bot-moderator/
├── bot/
│   ├── __init__.py
│   └── bot.py              # Основной файл запуска
├── filters/
│   ├── __init__.py
│   └── profanity.py        # Фильтр нецензурной лексики
├── handlers/
│   ├── __init__.py
│   └── moderation.py       # Обработчики команд и модерации
├── logging_config/
│   ├── __init__.py
│   └── config.py           # Настройка логирования
├── utils/
│   ├── __init__.py
│   ├── db.py              # Работа с базой данных
│   └── env.py             # Загрузка переменных окружения
├── docker-compose.yml     # Docker Compose конфигурация
├── Dockerfile            # Docker образ
├── requirements.txt      # Python зависимости
├── EnvExample           # Пример переменных окружения
├── setup_db.sql         # SQL скрипт для создания БД
└── README.md            # Документация
```

## 🔧 Настройка

### Добавление новых слов в фильтр
Отредактируйте `filters/profanity.py`:
```python
PROFANITY_LIST = [
    'бля', 'блять', 'сука', 'хуй', 'пизд', 'еба', 'ебл', 'муд',
    # Добавьте свои слова здесь
]
```

### Изменение правил чата
Отредактируйте `handlers/moderation.py`:
```python
RULES_TEXT = (
    "<b>Правила чата:</b>\n"
    "1. Запрещена нецензурная лексика и оскорбления.\n"
    # Измените правила здесь
)
```

## 📊 Мониторинг

### Просмотр логов
```bash
# Все логи
docker-compose logs bot

# Последние 50 строк
docker-compose logs bot --tail=50

# Логи в реальном времени
docker-compose logs -f bot
```

### Статистика в БД
```sql
-- Общая статистика
SELECT COUNT(*) as total_actions FROM bot_actions;

-- Статистика по типам действий
SELECT action_type, COUNT(*) FROM bot_actions GROUP BY action_type;

-- Топ пользователей по активности
SELECT user_id, COUNT(*) FROM bot_actions GROUP BY user_id ORDER BY COUNT(*) DESC;
```

## 🐛 Устранение неполадок

### Бот не реагирует на сообщения
1. Проверьте, что бот добавлен в группу как администратор
2. Убедитесь, что отключён Privacy Mode
3. Проверьте логи: `docker-compose logs bot`

### Ошибки подключения к БД
1. Проверьте параметры в `.env`
2. Убедитесь, что PostgreSQL сервер доступен
3. Проверьте права доступа пользователя БД

### Фильтр мата не работает
1. Проверьте список слов в `filters/profanity.py`
2. Убедитесь, что бот имеет права на удаление сообщений
3. Проверьте логи на наличие ошибок

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
- Создайте Issue в GitHub
- Обратитесь к документации aiogram
- Проверьте логи бота

---

**Создано с ❤️ для модерации Telegram чатов** 