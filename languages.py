# Словари с переводами для разных языков

TRANSLATIONS = {
    'ru': {
        # Основные
        'tasks': '📋 Мои задачи',
        'expenses': '💰 Расходы',
        'timer': '⏰ Таймер',
        'stats': '📊 Статистика',
        'settings': '⚙️ Настройки',
        'back': '◀️ Назад',
        'cancel': '❌ Отмена',
        'save': '💾 Сохранить',

        # Раздел задач
        'add_task': '➕ Добавить задачу',
        'tasks_today': '📅 На сегодня',
        'tasks_all': '📌 Все задачи',
        'tasks_done': '✅ Выполненные',
        'task_title': '📝 Введи название задачи:',
        'task_description': '📝 Введи описание (или "-" чтобы пропустить):',
        'task_due_date': '📅 Выбери срок выполнения:',
        'task_priority': '⚡ Выбери приоритет:',
        'task_category': '📁 Выбери категорию:',
        'priority_high': '🔴 Высокий',
        'priority_medium': '🟡 Средний',
        'priority_low': '🟢 Низкий',
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'week': 'На неделе',
        'skip': 'Пропустить',

        # Категории задач
        'cat_work': 'Работа',
        'cat_study': 'Учеба',
        'cat_home': 'Дом',
        'cat_health': 'Здоровье',
        'cat_finance': 'Финансы',
        'cat_shopping': 'Покупки',
        'cat_friends': 'Друзья',
        'cat_other': 'Другое',

        # Раздел расходов
        'add_expense': '➕ Добавить расход',
        'expenses_today': '📊 За сегодня',
        'expenses_week': '📅 За неделю',
        'expenses_month': '📈 За месяц',
        'expenses_categories': '📁 По категориям',
        'enter_amount': '💰 Введи сумму:',
        'choose_currency': '💱 Выбери валюту:',
        'choose_category': '📁 Выбери категорию:',
        'enter_description': '📝 Введи описание (или "-" чтобы пропустить):',

        # Категории расходов
        'exp_cat_food': '🍔 Еда',
        'exp_cat_transport': '🚇 Транспорт',
        'exp_cat_housing': '🏠 Жилье',
        'exp_cat_comm': '📱 Связь',
        'exp_cat_entertainment': '🎮 Развлечения',
        'exp_cat_clothing': '👕 Одежда',
        'exp_cat_health': '💊 Здоровье',
        'exp_cat_education': '📚 Образование',
        'exp_cat_gifts': '🎁 Подарки',
        'exp_cat_work': '💼 Работа',
        'exp_cat_pets': '🐱 Питомцы',
        'exp_cat_travel': '✈️ Путешествия',

        # Валюты
        'currency_rub': '🇷🇺 RUB (₽)',
        'currency_usd': '🇺🇸 USD ($)',
        'currency_eur': '🇪🇺 EUR (€)',
        'currency_uah': '🇺🇦 UAH (₴)',

        # Таймер
        'timer_start': '▶️ Старт',
        'timer_pause': '⏸️ Пауза',
        'timer_stop': '⏹️ Стоп',
        'timer_resume': '▶️ Продолжить',
        'timer_settings': '⚙️ Настройки таймера',
        'timer_stats': '📊 Статистика',
        'timer_work': '💼 Работа',
        'timer_break': '☕ Перерыв',
        'timer_long_break': '🌴 Длинный перерыв',
        'timer_cycles': '🔄 Циклов',

        # Настройки
        'language': '🌐 Язык',
        'currency': '💱 Валюта по умолчанию',
        'notifications': '🔔 Уведомления',
        'choose_language': '🌐 Выбери язык:',
        'timer_duration': '⏱ Длительность',
        'timer_work_duration': '⏱ Работа (минут):',
        'timer_break_duration': '⏱ Перерыв (минут):',
        'timer_long_break_duration': '⏱ Длинный перерыв (минут):',
        'notifications_on': '🔔 Уведомления включены',
        'notifications_off': '🔕 Уведомления выключены',
        'reminder_time': '⏰ Время напоминания:',

        # Языки
        'lang_ru': '🇷🇺 Русский',
        'lang_en': '🇬🇧 English',
        'lang_uk': '🇺🇦 Українська',

        # Сообщения
        'welcome': '🌟 <b>Productivity Bot</b> — твой персональный помощник!\n\nПривет, {name}! Я помогу тебе управлять задачами, расходами и временем.',
        'task_added': '✅ <b>Задача добавлена!</b>\n\n📌 <b>{title}</b>\n📁 Категория: {category}\n⚡ Приоритет: {priority}\n📅 Срок: {due_date}',
        'expense_added': '✅ <b>Расход добавлен!</b>\n\n💰 Сумма: {amount} {currency}\n📁 Категория: {category}\n📝 Описание: {description}',
        'no_tasks': '📭 Нет задач',
        'no_expenses': '💰 Нет расходов',
        'total': 'Итого',
        'currency_changed': '✅ Валюта по умолчанию изменена на {currency}',
        'language_changed': '✅ Язык изменен на {language}',
        'timer_started': '▶️ <b>Таймер запущен!</b>\n\n⏱ Работа: {work} мин\n🔄 Цикл: {cycle}/4\n\n<i>Сфокусируйся на задаче!</i>',
        'timer_paused': '⏸️ <b>Таймер на паузе</b>\n\nОсталось: {remaining} мин',
        'timer_resumed': '▶️ <b>Таймер продолжен</b>\n\nОсталось: {remaining} мин',
        'timer_stopped': '⏹️ <b>Таймер остановлен</b>\n\n✅ Выполнено циклов: {cycles}',
        'work_completed': '🎉 <b>Рабочий цикл завершен!</b>\n\n✅ Выполнено циклов: {cycles}\n☕ {break_type} перерыв: {break_minutes} мин',
        'break_completed': '⏰ <b>Перерыв закончен!</b>\n\n🍅 Начинаем новый рабочий цикл {cycle}/4',
        'timer_settings_updated': '✅ Настройки таймера обновлены!\n\nРабота: {work} мин\nПерерыв: {break_} мин\nДлинный перерыв: {long_break} мин',
        'notifications_updated': '✅ Настройки уведомлений обновлены',
    },

    'en': {
        # Main
        'tasks': '📋 My Tasks',
        'expenses': '💰 Expenses',
        'timer': '⏰ Timer',
        'stats': '📊 Statistics',
        'settings': '⚙️ Settings',
        'back': '◀️ Back',
        'cancel': '❌ Cancel',
        'save': '💾 Save',

        # Tasks section
        'add_task': '➕ Add Task',
        'tasks_today': '📅 Today',
        'tasks_all': '📌 All Tasks',
        'tasks_done': '✅ Completed',
        'task_title': '📝 Enter task title:',
        'task_description': '📝 Enter description (or "-" to skip):',
        'task_due_date': '📅 Choose due date:',
        'task_priority': '⚡ Choose priority:',
        'task_category': '📁 Choose category:',
        'priority_high': '🔴 High',
        'priority_medium': '🟡 Medium',
        'priority_low': '🟢 Low',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'week': 'This week',
        'skip': 'Skip',

        # Task categories
        'cat_work': 'Work',
        'cat_study': 'Study',
        'cat_home': 'Home',
        'cat_health': 'Health',
        'cat_finance': 'Finance',
        'cat_shopping': 'Shopping',
        'cat_friends': 'Friends',
        'cat_other': 'Other',

        # Expenses section
        'add_expense': '➕ Add Expense',
        'expenses_today': '📊 Today',
        'expenses_week': '📅 This Week',
        'expenses_month': '📈 This Month',
        'expenses_categories': '📁 By Category',
        'enter_amount': '💰 Enter amount:',
        'choose_currency': '💱 Choose currency:',
        'choose_category': '📁 Choose category:',
        'enter_description': '📝 Enter description (or "-" to skip):',

        # Expense categories
        'exp_cat_food': '🍔 Food',
        'exp_cat_transport': '🚇 Transport',
        'exp_cat_housing': '🏠 Housing',
        'exp_cat_comm': '📱 Communication',
        'exp_cat_entertainment': '🎮 Entertainment',
        'exp_cat_clothing': '👕 Clothing',
        'exp_cat_health': '💊 Health',
        'exp_cat_education': '📚 Education',
        'exp_cat_gifts': '🎁 Gifts',
        'exp_cat_work': '💼 Work',
        'exp_cat_pets': '🐱 Pets',
        'exp_cat_travel': '✈️ Travel',

        # Currencies
        'currency_rub': '🇷🇺 RUB (₽)',
        'currency_usd': '🇺🇸 USD ($)',
        'currency_eur': '🇪🇺 EUR (€)',
        'currency_uah': '🇺🇦 UAH (₴)',

        # Timer
        'timer_start': '▶️ Start',
        'timer_pause': '⏸️ Pause',
        'timer_stop': '⏹️ Stop',
        'timer_resume': '▶️ Resume',
        'timer_settings': '⚙️ Timer Settings',
        'timer_stats': '📊 Statistics',
        'timer_work': '💼 Work',
        'timer_break': '☕ Break',
        'timer_long_break': '🌴 Long Break',
        'timer_cycles': '🔄 Cycles',

        # Settings
        'language': '🌐 Language',
        'currency': '💱 Default Currency',
        'notifications': '🔔 Notifications',
        'choose_language': '🌐 Choose language:',
        'timer_duration': '⏱ Duration',
        'timer_work_duration': '⏱ Work (minutes):',
        'timer_break_duration': '⏱ Break (minutes):',
        'timer_long_break_duration': '⏱ Long break (minutes):',
        'notifications_on': '🔔 Notifications on',
        'notifications_off': '🔕 Notifications off',
        'reminder_time': '⏰ Reminder time:',

        # Languages
        'lang_ru': '🇷🇺 Русский',
        'lang_en': '🇬🇧 English',
        'lang_uk': '🇺🇦 Українська',

        # Messages
        'welcome': '🌟 <b>Productivity Bot</b> — your personal assistant!\n\nHi, {name}! I will help you manage tasks, expenses and time.',
        'task_added': '✅ <b>Task added!</b>\n\n📌 <b>{title}</b>\n📁 Category: {category}\n⚡ Priority: {priority}\n📅 Due: {due_date}',
        'expense_added': '✅ <b>Expense added!</b>\n\n💰 Amount: {amount} {currency}\n📁 Category: {category}\n📝 Description: {description}',
        'no_tasks': '📭 No tasks',
        'no_expenses': '💰 No expenses',
        'total': 'Total',
        'currency_changed': '✅ Default currency changed to {currency}',
        'language_changed': '✅ Language changed to {language}',
        'timer_started': '▶️ <b>Timer started!</b>\n\n⏱ Work: {work} min\n🔄 Cycle: {cycle}/4\n\n<i>Focus on your task!</i>',
        'timer_paused': '⏸️ <b>Timer paused</b>\n\nRemaining: {remaining} min',
        'timer_resumed': '▶️ <b>Timer resumed</b>\n\nRemaining: {remaining} min',
        'timer_stopped': '⏹️ <b>Timer stopped</b>\n\n✅ Cycles completed: {cycles}',
        'work_completed': '🎉 <b>Work cycle completed!</b>\n\n✅ Cycles: {cycles}\n☕ {break_type} break: {break_minutes} min',
        'break_completed': '⏰ <b>Break finished!</b>\n\n🍅 Starting new work cycle {cycle}/4',
        'timer_settings_updated': '✅ Timer settings updated!\n\nWork: {work} min\nBreak: {break_} min\nLong break: {long_break} min',
        'notifications_updated': '✅ Notification settings updated',
    },

    'uk': {
        # Основні
        'tasks': '📋 Мої завдання',
        'expenses': '💰 Витрати',
        'timer': '⏰ Таймер',
        'stats': '📊 Статистика',
        'settings': '⚙️ Налаштування',
        'back': '◀️ Назад',
        'cancel': '❌ Скасувати',
        'save': '💾 Зберегти',

        # Розділ завдань
        'add_task': '➕ Додати завдання',
        'tasks_today': '📅 На сьогодні',
        'tasks_all': '📌 Всі завдання',
        'tasks_done': '✅ Виконані',
        'task_title': '📝 Введи назву завдання:',
        'task_description': '📝 Введи опис (або "-" щоб пропустити):',
        'task_due_date': '📅 Оберіть термін виконання:',
        'task_priority': '⚡ Оберіть пріоритет:',
        'task_category': '📁 Оберіть категорію:',
        'priority_high': '🔴 Високий',
        'priority_medium': '🟡 Середній',
        'priority_low': '🟢 Низький',
        'today': 'Сьогодні',
        'tomorrow': 'Завтра',
        'week': 'На цьому тижні',
        'skip': 'Пропустити',

        # Категорії завдань
        'cat_work': 'Робота',
        'cat_study': 'Навчання',
        'cat_home': 'Дім',
        'cat_health': "Здоров'я",
        'cat_finance': 'Фінанси',
        'cat_shopping': 'Покупки',
        'cat_friends': 'Друзі',
        'cat_other': 'Інше',

        # Розділ витрат
        'add_expense': '➕ Додати витрату',
        'expenses_today': '📊 За сьогодні',
        'expenses_week': '📅 За тиждень',
        'expenses_month': '📈 За місяць',
        'expenses_categories': '📁 За категоріями',
        'enter_amount': '💰 Введи суму:',
        'choose_currency': '💱 Оберіть валюту:',
        'choose_category': '📁 Оберіть категорію:',
        'enter_description': '📝 Введи опис (або "-" щоб пропустити):',

        # Категорії витрат
        'exp_cat_food': '🍔 Їжа',
        'exp_cat_transport': '🚇 Транспорт',
        'exp_cat_housing': '🏠 Житло',
        'exp_cat_comm': '📱 Зв\'язок',
        'exp_cat_entertainment': '🎮 Розваги',
        'exp_cat_clothing': '👕 Одяг',
        'exp_cat_health': '💊 Здоров\'я',
        'exp_cat_education': '📚 Освіта',
        'exp_cat_gifts': '🎁 Подарунки',
        'exp_cat_work': '💼 Робота',
        'exp_cat_pets': '🐱 Улюбленці',
        'exp_cat_travel': '✈️ Подорожі',

        # Валюти
        'currency_rub': '🇷🇺 RUB (₽)',
        'currency_usd': '🇺🇸 USD ($)',
        'currency_eur': '🇪🇺 EUR (€)',
        'currency_uah': '🇺🇦 UAH (₴)',

        # Таймер
        'timer_start': '▶️ Старт',
        'timer_pause': '⏸️ Пауза',
        'timer_stop': '⏹️ Стоп',
        'timer_resume': '▶️ Продовжити',
        'timer_settings': '⚙️ Налаштування таймера',
        'timer_stats': '📊 Статистика',
        'timer_work': '💼 Робота',
        'timer_break': '☕ Перерва',
        'timer_long_break': '🌴 Довга перерва',
        'timer_cycles': '🔄 Цикли',

        # Налаштування
        'language': '🌐 Мова',
        'currency': '💱 Валюта за замовчуванням',
        'notifications': '🔔 Сповіщення',
        'choose_language': '🌐 Оберіть мову:',
        'timer_duration': '⏱ Тривалість',
        'timer_work_duration': '⏱ Робота (хвилин):',
        'timer_break_duration': '⏱ Перерва (хвилин):',
        'timer_long_break_duration': '⏱ Довга перерва (хвилин):',
        'notifications_on': '🔔 Сповіщення увімкнено',
        'notifications_off': '🔕 Сповіщення вимкнено',
        'reminder_time': '⏰ Час нагадування:',

        # Мови
        'lang_ru': '🇷🇺 Русский',
        'lang_en': '🇬🇧 English',
        'lang_uk': '🇺🇦 Українська',

        # Повідомлення
        'welcome': '🌟 <b>Productivity Bot</b> — твій персональний помічник!\n\nПривіт, {name}! Я допоможу тобі керувати завданнями, витратами та часом.',
        'task_added': '✅ <b>Завдання додано!</b>\n\n📌 <b>{title}</b>\n📁 Категорія: {category}\n⚡ Пріоритет: {priority}\n📅 Термін: {due_date}',
        'expense_added': '✅ <b>Витрату додано!</b>\n\n💰 Сума: {amount} {currency}\n📁 Категорія: {category}\n📝 Опис: {description}',
        'no_tasks': '📭 Немає завдань',
        'no_expenses': '💰 Немає витрат',
        'total': 'Всього',
        'currency_changed': '✅ Валюту за замовчуванням змінено на {currency}',
        'language_changed': '✅ Мову змінено на {language}',
        'timer_started': '▶️ <b>Таймер запущено!</b>\n\n⏱ Робота: {work} хв\n🔄 Цикл: {cycle}/4\n\n<i>Зосередься на завданні!</i>',
        'timer_paused': '⏸️ <b>Таймер на паузі</b>\n\nЗалишилось: {remaining} хв',
        'timer_resumed': '▶️ <b>Таймер продовжено</b>\n\nЗалишилось: {remaining} хв',
        'timer_stopped': '⏹️ <b>Таймер зупинено</b>\n\n✅ Виконано циклів: {cycles}',
        'work_completed': '🎉 <b>Робочий цикл завершено!</b>\n\n✅ Циклів: {cycles}\n☕ {break_type} перерва: {break_minutes} хв',
        'break_completed': '⏰ <b>Перерва закінчилась!</b>\n\n🍅 Починаємо новий робочий цикл {cycle}/4',
        'timer_settings_updated': '✅ Налаштування таймера оновлено!\n\nРобота: {work} хв\nПерерва: {break_} хв\nДовга перерва: {long_break} хв',
        'notifications_updated': '✅ Налаштування сповіщень оновлено',
    }
}


def get_text(user_lang: str, key: str, **kwargs) -> str:
    """Получить текст на нужном языке с подстановкой параметров"""
    if user_lang not in TRANSLATIONS:
        user_lang = 'en'

    text = TRANSLATIONS[user_lang].get(key, TRANSLATIONS['en'].get(key, key))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text