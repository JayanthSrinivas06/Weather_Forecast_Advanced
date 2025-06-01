import sqlite3

DB_NAME = "weather_data.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                date TEXT,
                temp REAL,
                description TEXT,
                is_current INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def save_current_weather(city, date, temp, description):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO weather (city, date, temp, description, is_current)
            VALUES (?, ?, ?, ?, 1)
        ''', (city, date, temp, description))
        conn.commit()

def save_forecast_weather(forecast_list):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        for entry in forecast_list:
            c.execute('''
                INSERT INTO weather (city, date, temp, description, is_current)
                VALUES (?, ?, ?, ?, 0)
            ''', (entry['city'], entry['date'], entry['temp'], entry['description']))
        conn.commit()

def get_all_weather():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM weather ORDER BY date')
        return c.fetchall()

def update_weather_record(record_id, temp, description):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE weather
            SET temp = ?, description = ?
            WHERE id = ?
        ''', (temp, description, record_id))
        conn.commit()


def delete_weather_record(record_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM weather WHERE id = ?', (record_id,))
        conn.commit()

