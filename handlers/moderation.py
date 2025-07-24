import logging
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters import ProfanityFilter
from utils.db import log_action, get_chat_stats
from aiogram.enums import UpdateType

router = Router()
logger = logging.getLogger(__name__)

HELLO_TEXT = (
    "🛠 Помощь по использованию бота-модератора\n\n"
    "📎 Команды:\n"
    "/start — приветствие и описание бота  \n"
    "/help — показать это сообщение  \n"
    "/stats — статистика по чату (только для админов)  \n"
    "/rules — правила чата  \n"
    "---\n\n"
    "🔍 Функции модерации:\n"
    "- Автоматическое удаление сообщений с нецензурной лексикой  \n"
    "- Фильтрация спама и нежелательных ссылок  \n"
    "- Логирование всех действий в базу данных  \n"
    "---\n\n"
    "⚙️ Настройка:\n"
    "1. Добавьте бота в группу  \n"
    "2. Дайте боту права администратора  \n"
    "3. Включите право \"Удаление сообщений\"\n\n"
    "---\n\n"
    "📊 Примечание:\n"
    "Все действия бота записываются в логи для анализа."
)

RULES_TEXT = (
    "<b>Правила чата:</b>\n"
    "1. Запрещена нецензурная лексика и оскорбления.\n"
    "2. Не спамить и не размещать нежелательные ссылки.\n"
    "3. Соблюдайте уважение к участникам и администрации.\n"
    "4. Не нарушайте законы РФ и правила Telegram.\n"
    "5. Администрация оставляет за собой право удалять сообщения и участников без объяснения причин."
)

rules_kb = InlineKeyboardBuilder()
rules_kb.button(text="Показать правила", callback_data="show_rules")
rules_kb = rules_kb.as_markup()

@router.message(Command("start"))
@router.message(Command("help"))
async def cmd_start_help(message: types.Message):
    await message.reply(HELLO_TEXT, reply_markup=rules_kb)
    await log_action(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        action_type='command',
        action_description='Вызов команды /start или /help',
        message_text=message.text
    )
    logger.info(f"Пользователь {message.from_user.id} вызвал /start или /help.")

@router.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.reply(RULES_TEXT, parse_mode="HTML")
    await log_action(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        action_type='command',
        action_description='Запрос правил чата',
        message_text=message.text
    )
    logger.info(f"Пользователь {message.from_user.id} запросил /rules.")

@router.callback_query(F.data == "show_rules")
async def show_rules_callback(call: types.CallbackQuery):
    await call.message.answer(RULES_TEXT, parse_mode="HTML")
    await call.answer()
    await log_action(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        action_type='callback',
        action_description='Запрос правил через кнопку',
        message_text=None
    )
    logger.info(f"Пользователь {call.from_user.id} запросил правила через кнопку.")

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    member = await message.chat.get_member(message.from_user.id)
    if member.status in ["creator", "administrator"]:
        try:
            stats = await get_chat_stats(message.chat.id)
            stats_text = (
                "📊 <b>Статистика чата</b>\n\n"
                "📈 <b>Общая статистика:</b>\n"
                f"• Всего действий: {stats['total_actions']}\n"
                f"• Удалено сообщений: {stats['deleted_messages']}\n"
                f"• Уникальных пользователей: {stats['unique_users']}\n\n"
                "👮‍♂️ Бот активно работает и ведёт полную статистику всех действий."
            )
            await message.reply(stats_text, parse_mode="HTML")
            await log_action(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                action_type='command',
                action_description='Запрос статистики (админ)',
                message_text=message.text
            )
            logger.info(f"Админ {message.from_user.id} запросил /stats.")
        except Exception as e:
            await message.reply("❌ Ошибка при получении статистики.")
            logger.error(f"Ошибка при получении статистики: {e}")
    else:
        await message.reply("Только администраторы могут просматривать статистику.")
        await log_action(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            action_type='command',
            action_description='Попытка запроса статистики без прав админа',
            message_text=message.text
        )
        logger.info(f"Пользователь {message.from_user.id} попытался получить /stats без прав админа.")

@router.message(ProfanityFilter())
async def profanity_handler(message: types.Message):
    try:
        await message.delete()
        warning_text = f"⚠️ <b>Внимание!</b>\nПользователь @{message.from_user.username or message.from_user.first_name}, использование нецензурной лексики запрещено в этом чате. Сообщение удалено."
        await message.answer(warning_text, parse_mode="HTML")
        await log_action(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            action_type='profanity_filter',
            action_description='Удаление сообщения с нецензурной лексикой',
            message_text=message.text
        )
        logger.info(f"Удалено сообщение с матом от пользователя {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

@router.my_chat_member()
async def on_bot_added(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator") and event.old_chat_member.status == "left":
        try:
            await event.bot.send_message(event.chat.id, HELLO_TEXT, reply_markup=rules_kb)
            await log_action(
                user_id=event.from_user.id,
                chat_id=event.chat.id,
                action_type='bot_added',
                action_description='Бот добавлен в чат',
                message_text=None
            )
            logger.info(f"Бот добавлен в чат {event.chat.id}, отправлено приветствие.")
        except Exception as e:
            logger.error(f"Ошибка при отправке приветствия: {e}")

@router.callback_query()
async def catch_all_callback(call: types.CallbackQuery):
    logger.warning(f"Необработанный callback_query: {call.data}")
    await call.answer("Неизвестная кнопка.") 