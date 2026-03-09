from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from languages import get_text


def get_main_keyboard(user_lang: str = 'en'):
    """Главная клавиатура с учетом языка"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=get_text(user_lang, 'tasks')))
    builder.add(KeyboardButton(text=get_text(user_lang, 'expenses')))
    builder.add(KeyboardButton(text=get_text(user_lang, 'timer')))
    builder.add(KeyboardButton(text=get_text(user_lang, 'stats')))
    builder.add(KeyboardButton(text=get_text(user_lang, 'settings')))
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_tasks_keyboard(user_lang: str = 'en'):
    """Клавиатура для раздела задач"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'add_task'), callback_data="add_task"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'tasks_today'), callback_data="tasks_today"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'tasks_all'), callback_data="tasks_all"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'tasks_done'), callback_data="tasks_done"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_main"))
    builder.adjust(1)
    return builder.as_markup()


def get_expenses_keyboard(user_lang: str = 'en'):
    """Клавиатура для раздела расходов"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'add_expense'), callback_data="add_expense"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'expenses_today'), callback_data="expenses_today"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'expenses_week'), callback_data="expenses_week"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'expenses_month'), callback_data="expenses_month"))
    builder.add(
        InlineKeyboardButton(text=get_text(user_lang, 'expenses_categories'), callback_data="expenses_categories"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_main"))
    builder.adjust(1)
    return builder.as_markup()


def get_timer_keyboard(user_lang: str = 'en'):
    """Клавиатура для таймера"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_start'), callback_data="timer_start"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_pause'), callback_data="timer_pause"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_stop'), callback_data="timer_stop"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_stats'), callback_data="timer_stats"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_settings'), callback_data="timer_settings_menu"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_main"))
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def get_settings_keyboard(user_lang: str = 'en'):
    """Клавиатура для настроек"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'language'), callback_data="settings_language"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency'), callback_data="settings_currency"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'notifications'), callback_data="settings_notifications"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'timer_settings'), callback_data="timer_settings_menu"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_main"))
    builder.adjust(1)
    return builder.as_markup()


def get_timer_settings_keyboard(user_lang: str = 'en'):
    """Клавиатура для настроек таймера"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="⏱ " + get_text(user_lang, 'timer_work_duration'), callback_data="timer_set_work"))
    builder.add(
        InlineKeyboardButton(text="☕ " + get_text(user_lang, 'timer_break_duration'), callback_data="timer_set_break"))
    builder.add(InlineKeyboardButton(text="🌴 " + get_text(user_lang, 'timer_long_break_duration'),
                                     callback_data="timer_set_long_break"))
    builder.add(
        InlineKeyboardButton(text="🔔 " + get_text(user_lang, 'notifications'), callback_data="timer_set_notifications"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_settings"))
    builder.adjust(1)
    return builder.as_markup()


def get_notifications_keyboard(user_lang: str = 'en'):
    """Клавиатура для настройки уведомлений"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'notifications_on'), callback_data="notif_on"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'notifications_off'), callback_data="notif_off"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_settings"))
    builder.adjust(1)
    return builder.as_markup()


def get_currency_keyboard(user_lang: str = 'en'):
    """Клавиатура для выбора валюты"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_rub'), callback_data="set_currency_RUB"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_usd'), callback_data="set_currency_USD"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_eur'), callback_data="set_currency_EUR"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_uah'), callback_data="set_currency_UAH"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_settings"))
    builder.adjust(1)
    return builder.as_markup()


def get_language_keyboard():
    """Клавиатура для выбора языка"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"))
    builder.add(InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"))
    builder.add(InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_lang_uk"))
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_settings"))
    builder.adjust(1)
    return builder.as_markup()


def get_categories_keyboard(user_lang: str = 'en'):
    """Клавиатура категорий расходов"""
    categories = [
        ('exp_cat_food', '🍔'),
        ('exp_cat_transport', '🚇'),
        ('exp_cat_housing', '🏠'),
        ('exp_cat_comm', '📱'),
        ('exp_cat_entertainment', '🎮'),
        ('exp_cat_clothing', '👕'),
        ('exp_cat_health', '💊'),
        ('exp_cat_education', '📚'),
        ('exp_cat_gifts', '🎁'),
        ('exp_cat_work', '💼'),
        ('exp_cat_pets', '🐱'),
        ('exp_cat_travel', '✈️')
    ]

    builder = InlineKeyboardBuilder()
    for cat_key, emoji in categories:
        cat_text = get_text(user_lang, cat_key)
        builder.add(InlineKeyboardButton(
            text=f"{emoji} {cat_text}",
            callback_data=f"expcat_{cat_key}"
        ))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_expenses"))
    builder.adjust(2)
    return builder.as_markup()


def get_expense_currency_keyboard(user_lang: str = 'en'):
    """Клавиатура для выбора валюты при добавлении расхода"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_rub'), callback_data="expcurrency_RUB"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_usd'), callback_data="expcurrency_USD"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_eur'), callback_data="expcurrency_EUR"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'currency_uah'), callback_data="expcurrency_UAH"))
    builder.adjust(1)
    return builder.as_markup()


def get_priority_keyboard(user_lang: str = 'en'):
    """Клавиатура для выбора приоритета задачи"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'priority_high'), callback_data="priority_high"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'priority_medium'), callback_data="priority_medium"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'priority_low'), callback_data="priority_low"))
    builder.adjust(1)
    return builder.as_markup()


def get_date_keyboard(user_lang: str = 'en'):
    """Клавиатура для выбора даты"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'today'), callback_data="date_today"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'tomorrow'), callback_data="date_tomorrow"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'week'), callback_data="date_week"))
    builder.add(InlineKeyboardButton(text=get_text(user_lang, 'skip'), callback_data="date_skip"))
    builder.adjust(2)
    return builder.as_markup()


def get_task_categories_keyboard(user_lang: str = 'en'):
    """Клавиатура категорий задач"""
    categories = [
        ('cat_work', '💼'),
        ('cat_study', '📚'),
        ('cat_home', '🏠'),
        ('cat_health', '💊'),
        ('cat_finance', '💰'),
        ('cat_shopping', '🛒'),
        ('cat_friends', '👥'),
        ('cat_other', '📌')
    ]

    builder = InlineKeyboardBuilder()
    for cat_key, emoji in categories:
        cat_text = get_text(user_lang, cat_key)
        builder.add(InlineKeyboardButton(
            text=f"{emoji} {cat_text}",
            callback_data=f"taskcat_{cat_key}"
        ))
    builder.adjust(2)
    return builder.as_markup()