
import pytest

from src.data_loader import load_customer_data
from src.data_validator import validate_customer


def test_load_customer_json():

    data = load_customer_data()

    assert len(data["customers"]) == 3


def test_valid_customer_data():

    customer = {
        "customer_id": "C1001",
        "name": "John Smith",
        "address": "Newport",
        "meter_id": "M1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    assert validate_customer(customer) is True


def test_missing_customer_id():

    customer = {
        "name": "John Smith",
        "address": "Newport",
        "meter_id": "M1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    with pytest.raises(ValueError):
        validate_customer(customer)


def test_current_reading_lower_than_previous():

    customer = {
        "customer_id": "C1001",
        "name": "John Smith",
        "address": "Newport",
        "meter_id": "M1001",
        "previous_reading": 1250,
        "current_reading": 1000,
        "unit_rate": 0.25
    }

    with pytest.raises(ValueError):
        validate_customer(customer)


def test_negative_unit_rate():

    customer = {
        "customer_id": "C1001",
        "name": "John Smith",
        "address": "Newport",
        "meter_id": "M1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": -0.25
    }

    with pytest.raises(ValueError):
        validate_customer(customer)


def test_empty_customer_name():

    customer = {
        "customer_id": "C1001",
        "name": " ",
        "address": "Newport",
        "meter_id": "M1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    with pytest.raises(ValueError):
        validate_customer(customer)
