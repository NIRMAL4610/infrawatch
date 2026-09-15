import sqlite3
from datetime import datetime
from .config import load_config

def create_database():
    config = load_config()
    db_path = config["database"]["path"]

    connection = sqlite3.connect(db_path)
    
    connection.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu REAL,
                memory REAL,
                disk REAL,
                status TEXT
                )
                      """)
    
    connection.commit()
    connection.close()

def insert_metrics(cpu, memory, disk, status):
    connection = sqlite3.connect("data/infrawatch.db")

    connection.execute(
        """
        INSERT INTO metrics (timestamp, cpu, memory, disk, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cpu, memory, disk, status)
    )

    connection.commit()
    connection.close()

def get_metrics():
    connection = sqlite3.connect("data/infrawatch.db")

    cursor = connection.execute(
        "SELECT * FROM metrics"
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_high_cpu_metrics():
    connection = sqlite3.connect("data/infrawatch.db")

    cursor = connection.execute(
        "SELECT * FROM metrics WHERE cpu > ?",
        (40,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def save_metrics(cpu, memory, disk, status):
    insert_metrics(cpu, memory, disk, status)

def get_recent_metrics(limit=10):
    connection = sqlite3.connect("data/infrawatch.db")

    cursor = connection.execute(
        """
        SELECT timestamp, cpu, memory, disk, status
        FROM metrics
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    connection.close()

    return rows
