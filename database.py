import sqlite3
import aiosqlite
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional, Dict
import logging
import asyncio

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path="productivity.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Инициализация таблиц"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Таблица пользователей
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Таблица задач
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT,
                        description TEXT,
                        due_date DATE,
                        priority TEXT DEFAULT 'medium',
                        category TEXT DEFAULT 'other',
                        completed BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')

                # Таблица расходов
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        currency TEXT DEFAULT 'RUB',
                        category TEXT,
                        description TEXT,
                        date DATE DEFAULT CURRENT_DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')

                # Таблица сессий таймера
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS timer_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        task_id INTEGER,
                        duration INTEGER,
                        completed BOOLEAN DEFAULT 1,
                        date DATE DEFAULT CURRENT_DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                        FOREIGN KEY (task_id) REFERENCES tasks (id)
                    )
                ''')

                # Таблица настроек пользователей
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_settings (
                        user_id INTEGER PRIMARY KEY,
                        language TEXT DEFAULT 'en',
                        default_currency TEXT DEFAULT 'RUB',
                        timer_work INTEGER DEFAULT 25,
                        timer_break INTEGER DEFAULT 5,
                        timer_long_break INTEGER DEFAULT 15,
                        daily_reminder BOOLEAN DEFAULT 0,
                        reminder_time TEXT DEFAULT '09:00',
                        notifications_enabled BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')

                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    # ============ МЕТОДЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ============

    async def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Добавление нового пользователя"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, username, first_name, last_name))
                await db.commit()
        except Exception as e:
            logger.error(f"Error adding user: {e}")

    # ============ МЕТОДЫ ДЛЯ ЗАДАЧ ============

    async def add_task(self, user_id: int, title: str, due_date: Optional[str] = None,
                       priority: str = "medium", category: str = "other", description: str = "") -> Optional[int]:
        """Добавление задачи"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                    INSERT INTO tasks (user_id, title, description, due_date, priority, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, title, description, due_date, priority, category))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return None

    async def get_tasks(self, user_id: int, completed: bool = False,
                        due_date: Optional[str] = None) -> List:
        """Получение задач"""
        try:
            completed_int = 1 if completed else 0
            query = 'SELECT id, title, description, due_date, priority, category FROM tasks WHERE user_id = ? AND completed = ?'
            params = [user_id, completed_int]

            if due_date:
                query += ' AND due_date = ?'
                params.append(due_date)

            query += ' ORDER BY due_date ASC, priority DESC, created_at DESC'

            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            return []

    async def get_all_tasks(self, user_id: int, include_completed: bool = False) -> List:
        """Получение всех задач пользователя"""
        try:
            query = 'SELECT id, title, description, due_date, priority, category, completed FROM tasks WHERE user_id = ?'
            params = [user_id]

            if not include_completed:
                query += ' AND completed = 0'

            query += ' ORDER BY due_date ASC, priority DESC, created_at DESC'

            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all tasks: {e}")
            return []

    async def complete_task(self, task_id: int) -> bool:
        """Отметить задачу выполненной"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return False

    async def delete_task(self, task_id: int) -> bool:
        """Удалить задачу"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return False

    async def get_task(self, task_id: int) -> Optional[Dict]:
        """Получить задачу по ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting task: {e}")
            return None

    # ============ МЕТОДЫ ДЛЯ РАСХОДОВ ============

    async def add_expense(self, user_id: int, amount: float, currency: str, category: str, description: str = "") -> \
    Optional[int]:
        """Добавление расхода с валютой"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                    INSERT INTO expenses (user_id, amount, currency, category, description, date)
                    VALUES (?, ?, ?, ?, ?, DATE('now'))
                ''', (user_id, amount, currency, category, description))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding expense: {e}")
            return None

    async def get_expenses(self, user_id: int, period: str = "day") -> List:
        """Получение расходов за период"""
        try:
            date_filter = {
                "day": "date = DATE('now')",
                "week": "date >= DATE('now', '-7 days')",
                "month": "date >= DATE('now', '-30 days')"
            }

            query = f'''
                SELECT id, amount, currency, category, description, date 
                FROM expenses 
                WHERE user_id = ? AND {date_filter.get(period, "date = DATE('now')")}
                ORDER BY date DESC, id DESC
            '''

            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, (user_id,))
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting expenses: {e}")
            return []

    async def get_expenses_by_category(self, user_id: int, period: str = "month") -> List:
        """Получение расходов по категориям"""
        try:
            date_filter = {
                "day": "date = DATE('now')",
                "week": "date >= DATE('now', '-7 days')",
                "month": "date >= DATE('now', '-30 days')"
            }

            query = f'''
                SELECT category, currency, SUM(amount) as total, COUNT(*) as count
                FROM expenses
                WHERE user_id = ? AND {date_filter.get(period, "date >= DATE('now', '-30 days')")}
                GROUP BY category, currency
                ORDER BY total DESC
            '''

            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(query, (user_id,))
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting expenses by category: {e}")
            return []

    async def get_total_expenses(self, user_id: int, period: str = "month") -> Dict[str, float]:
        """Получение общей суммы расходов по валютам"""
        try:
            date_filter = {
                "day": "date = DATE('now')",
                "week": "date >= DATE('now', '-7 days')",
                "month": "date >= DATE('now', '-30 days')"
            }

            query = f'''
                SELECT currency, SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND {date_filter.get(period, "date >= DATE('now', '-30 days')")}
                GROUP BY currency
            '''

            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(query, (user_id,))
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows} if rows else {}
        except Exception as e:
            logger.error(f"Error getting total expenses: {e}")
            return {}

    # ============ МЕТОДЫ ДЛЯ ТАЙМЕРА ============

    async def add_timer_session(self, user_id: int, duration: int, task_id: Optional[int] = None) -> Optional[int]:
        """Добавление сессии таймера"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                    INSERT INTO timer_sessions (user_id, task_id, duration)
                    VALUES (?, ?, ?)
                ''', (user_id, task_id, duration))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding timer session: {e}")
            return None

    async def get_timer_stats(self, user_id: int, period: str = "month") -> Dict:
        """Получение статистики таймера"""
        try:
            date_filter = {
                "day": "date = DATE('now')",
                "week": "date >= DATE('now', '-7 days')",
                "month": "date >= DATE('now', '-30 days')"
            }

            query = f'''
                SELECT COUNT(*) as sessions, SUM(duration) as total_minutes
                FROM timer_sessions
                WHERE user_id = ? AND {date_filter.get(period, "date >= DATE('now', '-30 days')")}
            '''

            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return {"sessions": row[0] or 0, "total_minutes": row[1] or 0}
                return {"sessions": 0, "total_minutes": 0}
        except Exception as e:
            logger.error(f"Error getting timer stats: {e}")
            return {"sessions": 0, "total_minutes": 0}

    # ============ МЕТОДЫ ДЛЯ НАСТРОЕК ============

    async def get_user_settings(self, user_id: int) -> Dict:
        """Получение настроек пользователя"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
                settings = await cursor.fetchone()

                if not settings:
                    # Создаем настройки по умолчанию
                    await db.execute('''
                        INSERT INTO user_settings (user_id) VALUES (?)
                    ''', (user_id,))
                    await db.commit()

                    cursor = await db.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
                    settings = await cursor.fetchone()

                return dict(settings) if settings else {
                    'language': 'en',
                    'default_currency': 'RUB',
                    'timer_work': 25,
                    'timer_break': 5,
                    'timer_long_break': 15,
                    'daily_reminder': 0,
                    'reminder_time': '09:00',
                    'notifications_enabled': 1
                }
        except Exception as e:
            logger.error(f"Error getting user settings: {e}")
            return {
                'language': 'en',
                'default_currency': 'RUB',
                'timer_work': 25,
                'timer_break': 5,
                'timer_long_break': 15,
                'daily_reminder': 0,
                'reminder_time': '09:00',
                'notifications_enabled': 1
            }

    async def update_settings(self, user_id: int, **kwargs) -> bool:
        """Обновление настроек"""
        try:
            allowed_fields = ['language', 'default_currency', 'timer_work', 'timer_break',
                              'timer_long_break', 'daily_reminder', 'reminder_time', 'notifications_enabled']

            updates = []
            values = []
            for key, value in kwargs.items():
                if key in allowed_fields:
                    updates.append(f"{key} = ?")
                    values.append(value)

            if not updates:
                return False

            values.append(user_id)
            query = f"UPDATE user_settings SET {', '.join(updates)} WHERE user_id = ?"

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(query, values)
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return False

    async def set_language(self, user_id: int, language: str) -> bool:
        """Установка языка пользователя"""
        return await self.update_settings(user_id, language=language)

    async def set_default_currency(self, user_id: int, currency: str) -> bool:
        """Установка валюты по умолчанию"""
        return await self.update_settings(user_id, default_currency=currency)

    async def set_timer_settings(self, user_id: int, work: int, break_: int, long_break: int) -> bool:
        """Установка настроек таймера"""
        return await self.update_settings(
            user_id,
            timer_work=work,
            timer_break=break_,
            timer_long_break=long_break
        )

    async def set_notifications(self, user_id: int, enabled: bool) -> bool:
        """Включение/выключение уведомлений"""
        return await self.update_settings(user_id, notifications_enabled=1 if enabled else 0)