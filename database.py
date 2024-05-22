
import psycopg2
from psycopg2 import sql

CREATE_TABLES_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS Norms(
        equipment VARCHAR(50),
        work_type VARCHAR(50),
        setup_time INTEGER,
        productivity_per_hour INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Shifts(
        equipment VARCHAR(50),
        date DATE,
        shifts VARCHAR(50) -- e.g., '9,9,0'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Breaks(
        break_start TIME,
        break_duration INTEGER,
        shift_type VARCHAR(50) -- e.g., '9-hour' or '12-hour'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Planning(
        id SERIAL PRIMARY KEY,
        equipment VARCHAR(50),
        work_type VARCHAR(50),
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        actual_end_time TIMESTAMP,
        priority INTEGER
    )
    """
]


def connect():
    try:
        connection = psycopg2.connect(
            dbname="base.db",
            user="Ваня",
            password="пароль",
            host="localhost",  # или другой хост, если PostgreSQL развернут удаленно
            port="5432"        # или другой порт, если используется нестандартный порт
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None


def create_tables(connection):
    with connection.cursor() as cursor:
        for query in CREATE_TABLES_QUERIES:
            cursor.execute(query)
        connection.commit()


# Пример использования
if __name__ == "__main__":
    conn = connect()
    if conn:
        create_tables(conn)
        conn.close()
