import sqlite3
from pathlib import Path
from contextlib import closing

DB_PATH = Path(__file__).resolve().parent.parent / "energy_billing.db"


def get_connection(db_path=DB_PATH):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path=DB_PATH):
    with closing(get_connection(db_path)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS bills (
                    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT NOT NULL,
                    previous_reading INTEGER NOT NULL,
                    current_reading INTEGER NOT NULL,
                    consumption INTEGER NOT NULL,
                    unit_rate TEXT NOT NULL,
                    total_bill TEXT NOT NULL,
                    FOREIGN KEY (customer_id)
                        REFERENCES customers(customer_id),
                    CHECK (previous_reading >= 0),
                    CHECK (current_reading >= previous_reading),
                    CHECK (consumption >= 0)
                )
            """)


def save_bill(
    customer_id,
    previous_reading,
    current_reading,
    unit_rate,
    total_bill,
    db_path=DB_PATH
):
    consumption = current_reading - previous_reading

    with closing(get_connection(db_path)) as connection:
        with connection:
            connection.execute(
                "INSERT OR IGNORE INTO customers (customer_id) VALUES (?)",
                (customer_id,)
            )

            cursor = connection.execute("""
                INSERT INTO bills (
                    customer_id,
                    previous_reading,
                    current_reading,
                    consumption,
                    unit_rate,
                    total_bill
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                previous_reading,
                current_reading,
                consumption,
                str(unit_rate),
                str(total_bill)
            ))

            return cursor.lastrowid


def get_bill(bill_id, db_path=DB_PATH):
    with closing(get_connection(db_path)) as connection:
        row = connection.execute(
            "SELECT * FROM bills WHERE bill_id = ?",
            (bill_id,)
        ).fetchone()

        return dict(row) if row else None


def get_customer_bills(customer_id, db_path=DB_PATH):
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute(
            "SELECT * FROM bills WHERE customer_id = ? ORDER BY bill_id",
            (customer_id,)
        ).fetchall()

        return [dict(row) for row in rows]