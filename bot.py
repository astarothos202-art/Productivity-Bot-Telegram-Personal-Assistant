import logging
import asyncio
from datetime import datetime, date, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import Database
from keyboards import *
from languages import get_text

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()


# Состояния для FSM
class TaskStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_due_date = State()
    waiting_for_priority = State()
    waiting_for_category = State()


class ExpenseStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_currency = State()
    waiting_for_category = State()
    waiting_for_description = State()


class TimerStates(StatesGroup):
    waiting_for_work = State()
    waiting_for_break = State()
    waiting_for_long_break = State()
    waiting_for_reminder_time = State()


# Активные таймеры пользователей
active_timers = {}


# ============= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =============

async def get_user_lang(user_id: int) -> str:
    """Получить язык пользователя"""
    settings = await db.get_user_settings(user_id)
    return settings.get('language', 'en')


async def timer_worker(user_id: int, chat_id: int):
    """Фоновая задача для таймера"""
    while user_id in active_timers:
        timer_data = active_timers[user_id]
        now = datetime.now()

        if now >= timer_data['end_time']:
            # Время вышло
            settings = await db.get_user_settings(user_id)
            user_lang = settings.get('language', 'en')

            if timer_data['is_working']:
                # Завершили рабочий цикл
                timer_data['cycles_completed'] += 1
                timer_data['is_working'] = False

                # Сохраняем сессию
                await db.add_timer_session(
                    user_id=user_id,
                    duration=timer_data['work_minutes']
                )

                # Определяем длительность перерыва
                if timer_data['cycles_completed'] % 4 == 0:
                    break_minutes = timer_data['long_break_minutes']
                    break_type = get_text(user_lang, 'timer_long_break')
                else:
                    break_minutes = timer_data['break_minutes']
                    break_type = get_text(user_lang, 'timer_break')

                timer_data['end_time'] = now + timedelta(minutes=break_minutes)

                # Отправляем уведомление
                await bot.send_message(
                    chat_id,
                    get_text(
                        user_lang,
                        'work_completed',
                        cycles=timer_data['cycles_completed'],
                        break_type=break_type,
                        break_minutes=break_minutes
                    ),
                    parse_mode="HTML"
                )
            else:
                # Завершили перерыв
                timer_data['is_working'] = True
                timer_data['end_time'] = now + timedelta(minutes=timer_data['work_minutes'])

                # Отправляем уведомление
                await bot.send_message(
                    chat_id,
                    get_text(
                        user_lang,
                        'break_completed',
                        cycle=(timer_data['cycles_completed'] % 4) + 1
                    ),
                    parse_mode="HTML"
                )

        await asyncio.sleep(5)  # Проверяем каждые 5 секунд


# ============= КОМАНДЫ =============

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user = message.from_user

    # Добавляем пользователя в БД
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Получаем настройки и язык
    settings = await db.get_user_settings(user.id)
    user_lang = settings.get('language', 'en')

    welcome_text = get_text(user_lang, 'welcome', name=user.first_name)

    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(user_lang),
        parse_mode="HTML"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    help_text = f"""
📚 <b>{get_text(user_lang, 'settings')}</b>

/start - {get_text(user_lang, 'welcome')}
/help - {get_text(user_lang, 'settings')}
/cancel - {get_text(user_lang, 'cancel')}
    """

    await message.answer(help_text, parse_mode="HTML")


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    current_state = await state.get_state()
    if current_state is None:
        await message.answer("🤷 " + get_text(user_lang, 'cancel'))
        return

    await state.clear()
    await message.answer(
        "❌ " + get_text(user_lang, 'cancel'),
        reply_markup=get_main_keyboard(user_lang)
    )


# ============= ОБРАБОТЧИКИ КНОПОК =============

@dp.message(lambda message: message.text in [get_text('ru', 'tasks'), get_text('en', 'tasks'), get_text('uk', 'tasks')])
async def tasks_section(message: Message):
    """Раздел задач"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    await message.answer(
        f"📋 <b>{get_text(user_lang, 'tasks')}</b>",
        reply_markup=get_tasks_keyboard(user_lang),
        parse_mode="HTML"
    )


@dp.message(lambda message: message.text in [get_text('ru', 'expenses'), get_text('en', 'expenses'),
                                             get_text('uk', 'expenses')])
async def expenses_section(message: Message):
    """Раздел расходов"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    await message.answer(
        f"💰 <b>{get_text(user_lang, 'expenses')}</b>",
        reply_markup=get_expenses_keyboard(user_lang),
        parse_mode="HTML"
    )


@dp.message(lambda message: message.text in [get_text('ru', 'timer'), get_text('en', 'timer'), get_text('uk', 'timer')])
async def timer_section(message: Message):
    """Раздел таймера"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    await message.answer(
        f"⏰ <b>{get_text(user_lang, 'timer')}</b>",
        reply_markup=get_timer_keyboard(user_lang),
        parse_mode="HTML"
    )


@dp.message(lambda message: message.text in [get_text('ru', 'stats'), get_text('en', 'stats'), get_text('uk', 'stats')])
async def stats_section(message: Message):
    """Раздел статистики"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    # Получаем статистику
    tasks_today = await db.get_tasks(user_id, completed=False, due_date=date.today().isoformat())
    tasks_all = await db.get_all_tasks(user_id, include_completed=False)
    tasks_completed = await db.get_tasks(user_id, completed=True)

    expenses_today = await db.get_expenses(user_id, "day")
    expenses_week = await db.get_expenses(user_id, "week")
    expenses_month = await db.get_expenses(user_id, "month")

    timer_stats = await db.get_timer_stats(user_id, "week")

    # Считаем суммы
    totals_today = await db.get_total_expenses(user_id, "day")
    totals_week = await db.get_total_expenses(user_id, "week")
    totals_month = await db.get_total_expenses(user_id, "month")

    # Символы валют
    currency_symbols = {
        'RUB': '₽',
        'USD': '$',
        'EUR': '€',
        'UAH': '₴'
    }

    today_total_text = ", ".join(
        [f"{total:.2f} {currency_symbols.get(curr, '')}" for curr, total in totals_today.items()])
    week_total_text = ", ".join(
        [f"{total:.2f} {currency_symbols.get(curr, '')}" for curr, total in totals_week.items()])
    month_total_text = ", ".join(
        [f"{total:.2f} {currency_symbols.get(curr, '')}" for curr, total in totals_month.items()])

    stats_text = f"""
📊 <b>{get_text(user_lang, 'stats')}</b>

📋 <b>{get_text(user_lang, 'tasks')}:</b>
• {get_text(user_lang, 'tasks_today')}: {len(tasks_today)}
• {get_text(user_lang, 'tasks_all')}: {len(tasks_all)}
• {get_text(user_lang, 'tasks_done')}: {len(tasks_completed)}

💰 <b>{get_text(user_lang, 'expenses')}:</b>
• {get_text(user_lang, 'expenses_today')}: {today_total_text if today_total_text else '0'}
• {get_text(user_lang, 'expenses_week')}: {week_total_text if week_total_text else '0'}
• {get_text(user_lang, 'expenses_month')}: {month_total_text if month_total_text else '0'}

⏰ <b>{get_text(user_lang, 'timer')}:</b>
• {get_text(user_lang, 'timer_stats')}: {timer_stats['sessions']} сессий
• {get_text(user_lang, 'total')}: {timer_stats['total_minutes']} мин
    """

    await message.answer(stats_text, parse_mode="HTML")


@dp.message(lambda message: message.text in [get_text('ru', 'settings'), get_text('en', 'settings'),
                                             get_text('uk', 'settings')])
async def settings_section(message: Message):
    """Раздел настроек"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)
    settings = await db.get_user_settings(user_id)

    # Названия языков
    lang_names = {'ru': 'Русский', 'en': 'English', 'uk': 'Українська'}

    # Названия валют
    currency_names = {
        'RUB': '🇷🇺 RUB',
        'USD': '🇺🇸 USD',
        'EUR': '🇪🇺 EUR',
        'UAH': '🇺🇦 UAH'
    }

    notif_status = get_text(user_lang, 'notifications_on') if settings.get('notifications_enabled', 1) else get_text(
        user_lang, 'notifications_off')

    settings_text = f"""
⚙️ <b>{get_text(user_lang, 'settings')}</b>

🌐 <b>{get_text(user_lang, 'language')}:</b> {lang_names.get(settings['language'], 'English')}
💱 <b>{get_text(user_lang, 'currency')}:</b> {currency_names.get(settings['default_currency'], 'RUB')}
⏰ <b>{get_text(user_lang, 'timer')}:</b> {settings['timer_work']}/{settings['timer_break']}/{settings['timer_long_break']} мин
🔔 <b>{get_text(user_lang, 'notifications')}:</b> {notif_status}
    """

    await message.answer(
        settings_text,
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )


# ============= НАСТРОЙКИ (ЯЗЫК И ВАЛЮТА) =============

@dp.callback_query(lambda c: c.data == "settings_language")
async def settings_language(callback: CallbackQuery):
    """Настройка языка"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'choose_language'),
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('set_lang_'))
async def set_language(callback: CallbackQuery):
    """Установка языка"""
    user_id = callback.from_user.id
    lang = callback.data.replace('set_lang_', '')

    # Сохраняем язык
    await db.set_language(user_id, lang)

    # Получаем название языка на выбранном языке
    lang_names = {
        'ru': 'Русский',
        'en': 'English',
        'uk': 'Українська'
    }

    await callback.message.edit_text(
        get_text(lang, 'language_changed', language=lang_names[lang]),
        reply_markup=get_settings_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "settings_currency")
async def settings_currency(callback: CallbackQuery):
    """Настройка валюты по умолчанию"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'choose_currency'),
        reply_markup=get_currency_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('set_currency_'))
async def set_default_currency(callback: CallbackQuery):
    """Установка валюты по умолчанию"""
    user_id = callback.from_user.id
    currency = callback.data.replace('set_currency_', '')

    # Получаем текущие настройки для языка
    user_lang = await get_user_lang(user_id)

    # Сохраняем валюту
    await db.set_default_currency(user_id, currency)

    # Названия валют
    currency_names = {
        'RUB': '🇷🇺 RUB',
        'USD': '🇺🇸 USD',
        'EUR': '🇪🇺 EUR',
        'UAH': '🇺🇦 UAH'
    }

    await callback.message.edit_text(
        get_text(user_lang, 'currency_changed', currency=currency_names[currency]),
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "settings_notifications")
async def settings_notifications(callback: CallbackQuery):
    """Настройка уведомлений"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        f"🔔 <b>{get_text(user_lang, 'notifications')}</b>",
        reply_markup=get_notifications_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "notif_on")
async def notifications_on(callback: CallbackQuery):
    """Включить уведомления"""
    user_id = callback.from_user.id
    await db.set_notifications(user_id, True)
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'notifications_updated'),
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "notif_off")
async def notifications_off(callback: CallbackQuery):
    """Выключить уведомления"""
    user_id = callback.from_user.id
    await db.set_notifications(user_id, False)
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'notifications_updated'),
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_settings_menu")
async def timer_settings_menu(callback: CallbackQuery):
    """Меню настроек таймера"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)
    settings = await db.get_user_settings(user_id)

    text = f"""
⚙️ <b>{get_text(user_lang, 'timer_settings')}</b>

{get_text(user_lang, 'timer_work_duration')} {settings['timer_work']}
{get_text(user_lang, 'timer_break_duration')} {settings['timer_break']}
{get_text(user_lang, 'timer_long_break_duration')} {settings['timer_long_break']}
    """

    await callback.message.edit_text(
        text,
        reply_markup=get_timer_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_set_work")
async def timer_set_work(callback: CallbackQuery, state: FSMContext):
    """Установка длительности работы"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'timer_work_duration') + "\n\nВведи количество минут (например: 25):",
        parse_mode="HTML"
    )
    await state.set_state(TimerStates.waiting_for_work)
    await callback.answer()


@dp.message(TimerStates.waiting_for_work)
async def process_timer_work(message: Message, state: FSMContext):
    """Обработка длительности работы"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    try:
        work = int(message.text)
        if work < 1 or work > 120:
            raise ValueError

        settings = await db.get_user_settings(user_id)
        await db.set_timer_settings(
            user_id,
            work,
            settings['timer_break'],
            settings['timer_long_break']
        )

        await message.answer(
            get_text(
                user_lang,
                'timer_settings_updated',
                work=work,
                break_=settings['timer_break'],
                long_break=settings['timer_long_break']
            ),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )
    except:
        await message.answer(
            "❌ Введи число от 1 до 120:"
        )

    await state.clear()


@dp.callback_query(lambda c: c.data == "timer_set_break")
async def timer_set_break(callback: CallbackQuery, state: FSMContext):
    """Установка длительности перерыва"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'timer_break_duration') + "\n\nВведи количество минут (например: 5):",
        parse_mode="HTML"
    )
    await state.set_state(TimerStates.waiting_for_break)
    await callback.answer()


@dp.message(TimerStates.waiting_for_break)
async def process_timer_break(message: Message, state: FSMContext):
    """Обработка длительности перерыва"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    try:
        break_ = int(message.text)
        if break_ < 1 or break_ > 60:
            raise ValueError

        settings = await db.get_user_settings(user_id)
        await db.set_timer_settings(
            user_id,
            settings['timer_work'],
            break_,
            settings['timer_long_break']
        )

        await message.answer(
            get_text(
                user_lang,
                'timer_settings_updated',
                work=settings['timer_work'],
                break_=break_,
                long_break=settings['timer_long_break']
            ),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )
    except:
        await message.answer(
            "❌ Введи число от 1 до 60:"
        )

    await state.clear()


@dp.callback_query(lambda c: c.data == "timer_set_long_break")
async def timer_set_long_break(callback: CallbackQuery, state: FSMContext):
    """Установка длительности длинного перерыва"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'timer_long_break_duration') + "\n\nВведи количество минут (например: 15):",
        parse_mode="HTML"
    )
    await state.set_state(TimerStates.waiting_for_long_break)
    await callback.answer()


@dp.message(TimerStates.waiting_for_long_break)
async def process_timer_long_break(message: Message, state: FSMContext):
    """Обработка длительности длинного перерыва"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    try:
        long_break = int(message.text)
        if long_break < 1 or long_break > 120:
            raise ValueError

        settings = await db.get_user_settings(user_id)
        await db.set_timer_settings(
            user_id,
            settings['timer_work'],
            settings['timer_break'],
            long_break
        )

        await message.answer(
            get_text(
                user_lang,
                'timer_settings_updated',
                work=settings['timer_work'],
                break_=settings['timer_break'],
                long_break=long_break
            ),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )
    except:
        await message.answer(
            "❌ Введи число от 1 до 120:"
        )

    await state.clear()


@dp.callback_query(lambda c: c.data == "back_settings")
async def back_to_settings(callback: CallbackQuery):
    """Вернуться в настройки"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    settings = await db.get_user_settings(user_id)
    lang_names = {'ru': 'Русский', 'en': 'English', 'uk': 'Українська'}
    currency_names = {
        'RUB': '🇷🇺 RUB',
        'USD': '🇺🇸 USD',
        'EUR': '🇪🇺 EUR',
        'UAH': '🇺🇦 UAH'
    }
    notif_status = get_text(user_lang, 'notifications_on') if settings.get('notifications_enabled', 1) else get_text(
        user_lang, 'notifications_off')

    settings_text = f"""
⚙️ <b>{get_text(user_lang, 'settings')}</b>

🌐 <b>{get_text(user_lang, 'language')}:</b> {lang_names.get(settings['language'], 'English')}
💱 <b>{get_text(user_lang, 'currency')}:</b> {currency_names.get(settings['default_currency'], 'RUB')}
⏰ <b>{get_text(user_lang, 'timer')}:</b> {settings['timer_work']}/{settings['timer_break']}/{settings['timer_long_break']} мин
🔔 <b>{get_text(user_lang, 'notifications')}:</b> {notif_status}
    """

    await callback.message.edit_text(
        settings_text,
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


# ============= ЗАДАЧИ =============

@dp.callback_query(lambda c: c.data == "add_task")
async def add_task_start(callback: CallbackQuery, state: FSMContext):
    """Начать добавление задачи"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'task_title'),
        parse_mode="HTML"
    )
    await state.set_state(TaskStates.waiting_for_title)
    await callback.answer()


@dp.message(TaskStates.waiting_for_title)
async def process_task_title(message: Message, state: FSMContext):
    """Обработка названия задачи"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    await state.update_data(title=message.text)
    await state.set_state(TaskStates.waiting_for_description)

    await message.answer(
        get_text(user_lang, 'task_description'),
        parse_mode="HTML"
    )


@dp.message(TaskStates.waiting_for_description)
async def process_task_description(message: Message, state: FSMContext):
    """Обработка описания задачи"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    if message.text != '-':
        await state.update_data(description=message.text)
    else:
        await state.update_data(description='')

    await state.set_state(TaskStates.waiting_for_due_date)

    await message.answer(
        get_text(user_lang, 'task_due_date'),
        reply_markup=get_date_keyboard(user_lang),
        parse_mode="HTML"
    )


@dp.callback_query(lambda c: c.data.startswith('date_'), TaskStates.waiting_for_due_date)
async def process_task_date_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора даты через кнопки"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    today = date.today()

    if callback.data == "date_today":
        due_date = today.isoformat()
    elif callback.data == "date_tomorrow":
        due_date = (today + timedelta(days=1)).isoformat()
    elif callback.data == "date_week":
        due_date = (today + timedelta(days=7)).isoformat()
    else:  # date_skip
        due_date = None

    await state.update_data(due_date=due_date)

    await callback.message.edit_text(
        get_text(user_lang, 'task_priority'),
        reply_markup=get_priority_keyboard(user_lang),
        parse_mode="HTML"
    )
    await state.set_state(TaskStates.waiting_for_priority)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('priority_'), TaskStates.waiting_for_priority)
async def process_task_priority(callback: CallbackQuery, state: FSMContext):
    """Обработка приоритета"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    priority = callback.data.replace('priority_', '')
    await state.update_data(priority=priority)

    await callback.message.edit_text(
        get_text(user_lang, 'task_category'),
        reply_markup=get_task_categories_keyboard(user_lang),
        parse_mode="HTML"
    )
    await state.set_state(TaskStates.waiting_for_category)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('taskcat_'), TaskStates.waiting_for_category)
async def process_task_category(callback: CallbackQuery, state: FSMContext):
    """Обработка категории и сохранение задачи"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    category_key = callback.data.replace('taskcat_', '')
    category = get_text(user_lang, category_key)
    data = await state.get_data()

    # Сохраняем задачу
    task_id = await db.add_task(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        due_date=data.get('due_date'),
        priority=data.get('priority', 'medium'),
        category=category
    )

    if task_id:
        await callback.message.edit_text(
            get_text(
                user_lang,
                'task_added',
                title=data['title'],
                category=category,
                priority=data.get('priority', 'medium'),
                due_date=data.get('due_date', get_text(user_lang, 'skip'))
            ),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text("❌ Error creating task")

    await state.clear()
    await callback.answer()


@dp.callback_query(lambda c: c.data == "tasks_today")
async def show_tasks_today(callback: CallbackQuery):
    """Показать задачи на сегодня"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    tasks = await db.get_tasks(user_id, completed=False, due_date=date.today().isoformat())

    if not tasks:
        await callback.message.edit_text(
            get_text(user_lang, 'no_tasks'),
            reply_markup=get_tasks_keyboard(user_lang)
        )
        await callback.answer()
        return

    # Создаем клавиатуру с задачами
    kb_builder = InlineKeyboardBuilder()
    for task in tasks:
        priority_emoji = '🔴' if task['priority'] == 'high' else '🟡' if task['priority'] == 'medium' else '🟢'
        kb_builder.add(InlineKeyboardButton(
            text=f"{priority_emoji} {task['title'][:30]}...",
            callback_data=f"view_task_{task['id']}"
        ))
    kb_builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_tasks"))
    kb_builder.adjust(1)

    await callback.message.edit_text(
        f"📋 <b>{get_text(user_lang, 'tasks_today')} ({len(tasks)}):</b>",
        reply_markup=kb_builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "tasks_all")
async def show_tasks_all(callback: CallbackQuery):
    """Показать все задачи"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    tasks = await db.get_all_tasks(user_id, include_completed=False)

    if not tasks:
        await callback.message.edit_text(
            get_text(user_lang, 'no_tasks'),
            reply_markup=get_tasks_keyboard(user_lang)
        )
        await callback.answer()
        return

    # Создаем клавиатуру с задачами
    kb_builder = InlineKeyboardBuilder()
    for task in tasks:
        priority_emoji = '🔴' if task['priority'] == 'high' else '🟡' if task['priority'] == 'medium' else '🟢'
        due_text = f" [{task['due_date']}]" if task['due_date'] else ""
        kb_builder.add(InlineKeyboardButton(
            text=f"{priority_emoji} {task['title'][:20]}...{due_text}",
            callback_data=f"view_task_{task['id']}"
        ))
    kb_builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_tasks"))
    kb_builder.adjust(1)

    await callback.message.edit_text(
        f"📋 <b>{get_text(user_lang, 'tasks_all')} ({len(tasks)}):</b>",
        reply_markup=kb_builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "tasks_done")
async def show_tasks_done(callback: CallbackQuery):
    """Показать выполненные задачи"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    tasks = await db.get_tasks(user_id, completed=True)

    if not tasks:
        await callback.message.edit_text(
            "✅ Нет выполненных задач",
            reply_markup=get_tasks_keyboard(user_lang)
        )
        await callback.answer()
        return

    # Создаем клавиатуру с задачами
    kb_builder = InlineKeyboardBuilder()
    for task in tasks:
        kb_builder.add(InlineKeyboardButton(
            text=f"✅ {task['title'][:30]}...",
            callback_data=f"view_task_{task['id']}"
        ))
    kb_builder.add(InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="back_tasks"))
    kb_builder.adjust(1)

    await callback.message.edit_text(
        f"✅ <b>{get_text(user_lang, 'tasks_done')} ({len(tasks)}):</b>",
        reply_markup=kb_builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('view_task_'))
async def view_task(callback: CallbackQuery):
    """Просмотр задачи"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    task_id = int(callback.data.replace('view_task_', ''))
    task = await db.get_task(task_id)

    if not task:
        await callback.answer("❌ Task not found")
        return

    # Эмодзи для приоритета
    priority_emoji = {
        'high': '🔴', 'medium': '🟡', 'low': '🟢'
    }

    status = "✅" if task['completed'] else "⏳"

    task_text = f"""
{status} <b>{task['title']}</b>

📁 {get_text(user_lang, 'task_category')}: {task['category']}
⚡ {get_text(user_lang, 'task_priority')}: {priority_emoji.get(task['priority'], '⚪')} {task['priority']}
📅 {get_text(user_lang, 'task_due_date')}: {task['due_date'] or get_text(user_lang, 'skip')}
📝 {get_text(user_lang, 'task_description')}: {task['description'] or get_text(user_lang, 'skip')}
    """

    kb_buttons = []
    if not task['completed']:
        kb_buttons.append([InlineKeyboardButton(text="✅ " + get_text(user_lang, 'tasks_done'),
                                                callback_data=f"complete_task_{task_id}")])
    kb_buttons.append(
        [InlineKeyboardButton(text="❌ " + get_text(user_lang, 'cancel'), callback_data=f"delete_task_{task_id}")])
    kb_buttons.append([InlineKeyboardButton(text=get_text(user_lang, 'back'), callback_data="tasks_all")])

    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)

    await callback.message.edit_text(
        task_text,
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('complete_task_'))
async def complete_task(callback: CallbackQuery):
    """Отметить задачу выполненной"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    task_id = int(callback.data.replace('complete_task_', ''))
    await db.complete_task(task_id)

    await callback.answer("✅ " + get_text(user_lang, 'tasks_done'))
    await show_tasks_all(callback)


@dp.callback_query(lambda c: c.data.startswith('delete_task_'))
async def delete_task(callback: CallbackQuery):
    """Удалить задачу"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    task_id = int(callback.data.replace('delete_task_', ''))
    await db.delete_task(task_id)

    await callback.answer("🗑 " + get_text(user_lang, 'cancel'))
    await show_tasks_all(callback)


@dp.callback_query(lambda c: c.data == "back_tasks")
async def back_to_tasks(callback: CallbackQuery):
    """Вернуться в раздел задач"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        f"📋 <b>{get_text(user_lang, 'tasks')}</b>",
        reply_markup=get_tasks_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


# ============= РАСХОДЫ =============

@dp.callback_query(lambda c: c.data == "add_expense")
async def add_expense_start(callback: CallbackQuery, state: FSMContext):
    """Начать добавление расхода"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        get_text(user_lang, 'enter_amount'),
        parse_mode="HTML"
    )
    await state.set_state(ExpenseStates.waiting_for_amount)
    await callback.answer()


@dp.message(ExpenseStates.waiting_for_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    """Обработка суммы расхода"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0:
            raise ValueError("Amount must be positive")

        await state.update_data(amount=amount)
        await state.set_state(ExpenseStates.waiting_for_currency)

        await message.answer(
            get_text(user_lang, 'choose_currency'),
            reply_markup=get_expense_currency_keyboard(user_lang),
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            "❌ " + get_text(user_lang, 'enter_amount')
        )


@dp.callback_query(lambda c: c.data.startswith('expcurrency_'), ExpenseStates.waiting_for_currency)
async def process_expense_currency(callback: CallbackQuery, state: FSMContext):
    """Обработка валюты расхода"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    currency = callback.data.replace('expcurrency_', '')
    await state.update_data(currency=currency)
    await state.set_state(ExpenseStates.waiting_for_category)

    await callback.message.edit_text(
        get_text(user_lang, 'choose_category'),
        reply_markup=get_categories_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('expcat_'), ExpenseStates.waiting_for_category)
async def process_expense_category(callback: CallbackQuery, state: FSMContext):
    """Обработка категории расхода"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    category_key = callback.data.replace('expcat_', '')
    await state.update_data(category_key=category_key)
    await state.set_state(ExpenseStates.waiting_for_description)

    await callback.message.edit_text(
        get_text(user_lang, 'enter_description'),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.message(ExpenseStates.waiting_for_description)
async def process_expense_description(message: Message, state: FSMContext):
    """Обработка описания и сохранение расхода"""
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    description = message.text if message.text != '-' else ''
    data = await state.get_data()

    # Получаем название категории на языке пользователя
    category_text = get_text(user_lang, data['category_key'])

    # Сохраняем расход
    expense_id = await db.add_expense(
        user_id=user_id,
        amount=data['amount'],
        currency=data['currency'],
        category=category_text,
        description=description
    )

    # Символы валют
    currency_symbols = {
        'RUB': '₽',
        'USD': '$',
        'EUR': '€',
        'UAH': '₴'
    }

    if expense_id:
        await message.answer(
            get_text(
                user_lang,
                'expense_added',
                amount=f"{data['amount']:.2f}",
                currency=currency_symbols.get(data['currency'], ''),
                category=category_text,
                description=description or '-'
            ),
            reply_markup=get_expenses_keyboard(user_lang),
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Error adding expense")

    await state.clear()


@dp.callback_query(lambda c: c.data == "expenses_today")
async def show_expenses_today(callback: CallbackQuery):
    """Показать расходы за сегодня"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    expenses = await db.get_expenses(user_id, "day")

    await show_expenses_list(callback, expenses, user_lang, "expenses_today")


@dp.callback_query(lambda c: c.data == "expenses_week")
async def show_expenses_week(callback: CallbackQuery):
    """Показать расходы за неделю"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    expenses = await db.get_expenses(user_id, "week")

    await show_expenses_list(callback, expenses, user_lang, "expenses_week")


@dp.callback_query(lambda c: c.data == "expenses_month")
async def show_expenses_month(callback: CallbackQuery):
    """Показать расходы за месяц"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    expenses = await db.get_expenses(user_id, "month")

    await show_expenses_list(callback, expenses, user_lang, "expenses_month")


@dp.callback_query(lambda c: c.data == "expenses_categories")
async def show_expenses_categories(callback: CallbackQuery):
    """Показать расходы по категориям"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    categories = await db.get_expenses_by_category(user_id, "month")

    if not categories:
        await callback.message.edit_text(
            get_text(user_lang, 'no_expenses'),
            reply_markup=get_expenses_keyboard(user_lang)
        )
        await callback.answer()
        return

    # Символы валют
    currency_symbols = {
        'RUB': '₽',
        'USD': '$',
        'EUR': '€',
        'UAH': '₴'
    }

    text = f"📁 <b>{get_text(user_lang, 'expenses_categories')}</b>\n\n"

    for cat in categories:
        text += f"• {cat['category']}: {cat['total']:.2f} {currency_symbols.get(cat['currency'], '')} ({cat['count']} шт.)\n"

    await callback.message.edit_text(
        text,
        reply_markup=get_expenses_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


async def show_expenses_list(callback: CallbackQuery, expenses: list, user_lang: str, period_key: str):
    """Показать список расходов"""
    if not expenses:
        await callback.message.edit_text(
            get_text(user_lang, 'no_expenses'),
            reply_markup=get_expenses_keyboard(user_lang)
        )
        await callback.answer()
        return

    # Символы валют
    currency_symbols = {
        'RUB': '₽',
        'USD': '$',
        'EUR': '€',
        'UAH': '₴'
    }

    # Группируем по датам
    by_date = {}
    for e in expenses:
        date_str = e['date']
        if date_str not in by_date:
            by_date[date_str] = []
        by_date[date_str].append(e)

    text = f"💰 <b>{get_text(user_lang, period_key)}</b>\n\n"

    totals = {}
    for date_str, date_expenses in sorted(by_date.items(), reverse=True):
        text += f"<b>{date_str}:</b>\n"
        for e in date_expenses:
            text += f"  • {e['amount']:.2f} {currency_symbols.get(e['currency'], '')} - {e['category']} - {e['description'] or '-'}\n"
            key = e['currency']
            totals[key] = totals.get(key, 0) + e['amount']
        text += "\n"

    text += "<b>" + get_text(user_lang, 'total') + ":</b> "
    total_texts = []
    for currency, total in totals.items():
        total_texts.append(f"{total:.2f} {currency_symbols.get(currency, '')}")
    text += ", ".join(total_texts)

    await callback.message.edit_text(
        text,
        reply_markup=get_expenses_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "back_expenses")
async def back_to_expenses(callback: CallbackQuery):
    """Вернуться в раздел расходов"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.edit_text(
        f"💰 <b>{get_text(user_lang, 'expenses')}</b>",
        reply_markup=get_expenses_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


# ============= ТАЙМЕР =============

@dp.callback_query(lambda c: c.data == "timer_start")
async def timer_start(callback: CallbackQuery, state: FSMContext):
    """Запуск таймера"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if user_id in active_timers:
        await callback.answer("⏰ Таймер уже запущен!")
        return

    settings = await db.get_user_settings(user_id)
    user_lang = settings.get('language', 'en')

    # Запускаем таймер
    active_timers[user_id] = {
        'work_minutes': settings['timer_work'],
        'break_minutes': settings['timer_break'],
        'long_break_minutes': settings['timer_long_break'],
        'cycles_completed': 0,
        'is_working': True,
        'end_time': datetime.now() + timedelta(minutes=settings['timer_work']),
        'task_id': None
    }

    # Запускаем фоновую задачу
    asyncio.create_task(timer_worker(user_id, chat_id))

    await callback.message.edit_text(
        get_text(
            user_lang,
            'timer_started',
            work=settings['timer_work'],
            cycle=1
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_lang, 'timer_pause'), callback_data="timer_pause"),
             InlineKeyboardButton(text=get_text(user_lang, 'timer_stop'), callback_data="timer_stop")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_pause")
async def timer_pause(callback: CallbackQuery):
    """Пауза таймера"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    if user_id not in active_timers:
        await callback.answer("Нет активного таймера")
        return

    timer_data = active_timers[user_id]
    remaining = int((timer_data['end_time'] - datetime.now()).total_seconds() / 60)

    await callback.message.edit_text(
        get_text(
            user_lang,
            'timer_paused',
            remaining=remaining
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_lang, 'timer_resume'), callback_data="timer_resume"),
             InlineKeyboardButton(text=get_text(user_lang, 'timer_stop'), callback_data="timer_stop")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_resume")
async def timer_resume(callback: CallbackQuery):
    """Продолжить таймер"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    if user_id not in active_timers:
        await callback.answer("Нет активного таймера")
        return

    timer_data = active_timers[user_id]
    remaining = int((timer_data['end_time'] - datetime.now()).total_seconds() / 60)

    await callback.message.edit_text(
        get_text(
            user_lang,
            'timer_resumed',
            remaining=remaining
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_lang, 'timer_pause'), callback_data="timer_pause"),
             InlineKeyboardButton(text=get_text(user_lang, 'timer_stop'), callback_data="timer_stop")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_stop")
async def timer_stop(callback: CallbackQuery):
    """Остановить таймер"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    cycles = 0
    if user_id in active_timers:
        cycles = active_timers[user_id]['cycles_completed']
        del active_timers[user_id]

    await callback.message.edit_text(
        get_text(
            user_lang,
            'timer_stopped',
            cycles=cycles
        ),
        reply_markup=get_timer_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "timer_stats")
async def timer_stats(callback: CallbackQuery):
    """Статистика таймера"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    stats_today = await db.get_timer_stats(user_id, "day")
    stats_week = await db.get_timer_stats(user_id, "week")
    stats_month = await db.get_timer_stats(user_id, "month")

    text = f"""
📊 <b>{get_text(user_lang, 'timer_stats')}</b>

📅 <b>{get_text(user_lang, 'expenses_today')}:</b>
• {get_text(user_lang, 'timer_stats')}: {stats_today['sessions']}
• {get_text(user_lang, 'total')}: {stats_today['total_minutes']} мин

📆 <b>{get_text(user_lang, 'expenses_week')}:</b>
• {get_text(user_lang, 'timer_stats')}: {stats_week['sessions']}
• {get_text(user_lang, 'total')}: {stats_week['total_minutes']} мин
• {get_text(user_lang, 'timer_work')}: {stats_week['total_minutes'] // max(stats_week['sessions'], 1)} мин/сессия

📈 <b>{get_text(user_lang, 'expenses_month')}:</b>
• {get_text(user_lang, 'timer_stats')}: {stats_month['sessions']}
• {get_text(user_lang, 'total')}: {stats_month['total_minutes']} мин
    """

    await callback.message.edit_text(
        text,
        reply_markup=get_timer_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


# ============= НАВИГАЦИЯ =============

@dp.callback_query(lambda c: c.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    """Вернуться в главное меню"""
    user_id = callback.from_user.id
    user_lang = await get_user_lang(user_id)

    await callback.message.delete()
    await callback.message.answer(
        get_text(user_lang, 'settings'),
        reply_markup=get_main_keyboard(user_lang)
    )
    await callback.answer()


# ============= ЗАПУСК =============

async def main():
    """Главная функция"""
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())