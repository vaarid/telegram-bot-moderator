# 🤝 Руководство по вкладу в проект

Спасибо за интерес к проекту Telegram Bot Moderator! Мы приветствуем вклад от сообщества.

## 🚀 Как внести вклад

### 1. Fork репозитория
1. Перейдите на [GitHub репозиторий](https://github.com/[ВАШ_USERNAME]/telegram-bot-moderator)
2. Нажмите кнопку "Fork" в правом верхнем углу
3. Склонируйте ваш fork локально:
   ```bash
   git clone https://github.com/[ВАШ_USERNAME]/telegram-bot-moderator.git
   cd telegram-bot-moderator
   ```

### 2. Создайте ветку для новой функции
```bash
git checkout -b feature/amazing-feature
# или для исправления бага
git checkout -b fix/bug-description
```

### 3. Внесите изменения
- Следуйте стилю кода проекта
- Добавьте комментарии к сложному коду
- Обновите документацию при необходимости
- Добавьте тесты для новой функциональности

### 4. Зафиксируйте изменения
```bash
git add .
git commit -m "Add: краткое описание изменений"
```

### 5. Отправьте изменения
```bash
git push origin feature/amazing-feature
```

### 6. Создайте Pull Request
1. Перейдите на GitHub
2. Нажмите "Compare & pull request"
3. Заполните шаблон PR
4. Ожидайте ревью

## 📋 Стандарты кода

### Python
- Следуйте [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Используйте type hints
- Добавляйте docstrings для функций и классов
- Максимальная длина строки: 88 символов (black)

### Git
- Используйте понятные сообщения коммитов
- Формат: `Type: краткое описание`
- Типы: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`

### Структура проекта
- Соблюдайте существующую структуру папок
- Добавляйте `__init__.py` в новые пакеты
- Обновляйте `requirements.txt` при добавлении зависимостей

## 🐛 Сообщение о багах

### Создание Issue
1. Проверьте, не был ли баг уже зарегистрирован
2. Создайте новое Issue с описанием:
   - Краткое описание проблемы
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версии: Python, aiogram, Docker
   - Логи ошибок

### Шаблон для багов
```markdown
## Описание бага
Краткое описание проблемы

## Шаги для воспроизведения
1. Шаг 1
2. Шаг 2
3. Шаг 3

## Ожидаемое поведение
Что должно происходить

## Фактическое поведение
Что происходит на самом деле

## Окружение
- Python: 3.10+
- aiogram: 3.x
- Docker: 20.10+
- OS: Ubuntu 20.04

## Логи
```
[Логи ошибок здесь]
```

## Дополнительная информация
Любая дополнительная информация
```

## 💡 Предложение новых функций

### Создание Feature Request
1. Опишите новую функцию
2. Объясните, почему она нужна
3. Предложите способ реализации
4. Укажите приоритет

### Шаблон для функций
```markdown
## Описание функции
Краткое описание новой функции

## Проблема
Какую проблему решает эта функция

## Предлагаемое решение
Как можно реализовать эту функцию

## Альтернативы
Какие альтернативные решения рассматривались

## Дополнительная информация
Любая дополнительная информация
```

## 🔧 Разработка

### Настройка окружения
1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Скопируйте `EnvExample` в `.env` и настройте
5. Запустите через Docker:
   ```bash
   docker-compose up --build
   ```

### Тестирование
- Добавляйте тесты для новой функциональности
- Используйте pytest для тестирования
- Проверяйте работу в Docker контейнере

### Документация
- Обновляйте README.md при изменении функциональности
- Добавляйте комментарии к коду
- Обновляйте примеры использования

## 📝 Ревью кода

### Для авторов PR
- Отвечайте на комментарии ревьюеров
- Вносите исправления в ту же ветку
- Обновляйте PR при необходимости

### Для ревьюеров
- Будьте конструктивными
- Указывайте на проблемы и предлагайте решения
- Проверяйте функциональность и безопасность

## 🏷 Версионирование

Проект использует [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Пример: `1.2.3`

## 📞 Поддержка

Если у вас есть вопросы:
- Создайте Issue с вопросом
- Обратитесь к документации
- Проверьте существующие Issues и PR

## 🎉 Благодарности

Спасибо всем, кто вносит вклад в проект! Ваша помощь делает проект лучше.

---

**Вместе мы создаём лучший инструмент для модерации Telegram чатов! 🚀** 