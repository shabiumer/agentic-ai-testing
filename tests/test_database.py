import sqlite3
import pytest

from src.database import (
    init_db,
    save_bill,
    get_bill,
    get_customer_bills
)


@pytest.fixture
def db_path(tmp_path):
    test_database = tmp_path / "test_billing.db"
    init_db(test_database)
    return test_database


def test_database_tables_created(db_path):
    with sqlite3.connect(db_path) as connection:
        tables = connection.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
        """).fetchall()

    table_names = [table[0] for table in tables]

    assert "customers" in table_names
    assert "bills" in table_names


def test_save_and_retrieve_bill(db_path):
    bill_id = save_bill(
        "C1001", 1000, 1250, "0.25", "62.50", db_path
    )

    result = get_bill(bill_id, db_path)

    assert result["customer_id"] == "C1001"
    assert result["consumption"] == 250
    assert result["total_bill"] == "62.50"


def test_unknown_bill_returns_none(db_path):
    result = get_bill(999, db_path)

    assert result is None


def test_get_customer_bills(db_path):
    save_bill("C1001", 1000, 1250, "0.25", "62.50", db_path)
    save_bill("C1002", 2000, 2300, "0.30", "90.00", db_path)

    results = get_customer_bills("C1001", db_path)

    assert len(results) == 1
    assert results[0]["customer_id"] == "C1001"


def test_multiple_bills_for_same_customer(db_path):
    save_bill("C1001", 1000, 1250, "0.25", "62.50", db_path)
    save_bill("C1001", 1250, 1500, "0.25", "62.50", db_path)

    results = get_customer_bills("C1001", db_path)

    assert len(results) == 2


def test_invalid_meter_reading_rejected(db_path):
    with pytest.raises(sqlite3.IntegrityError):
        save_bill(
            "C1001", 1250, 1000, "0.25", "0.00", db_path
        )