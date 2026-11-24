from src.database import get_customer_bills
import requests
from src.database import get_bill
from uuid import uuid4

BASE_URL = "http://127.0.0.1:8000"


def test_api_response_matches_database():
    customer_id = f"C{uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    # Step 1: Send API request
    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 201

    api_data = response.json()

    # Step 2: Retrieve the same bill from database
    database_data = get_bill(api_data["bill_id"])

    assert database_data is not None

    # Step 3: Compare API and database values
    assert api_data["bill_id"] == database_data["bill_id"]

    assert api_data["customer_id"] == database_data["customer_id"]

    assert api_data["consumption_kwh"] == database_data["consumption"]

    assert api_data["unit_rate"] == database_data["unit_rate"]

    assert api_data["total_bill"] == database_data["total_bill"]

def test_invalid_request_is_not_saved():
    customer_id = f"C{uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": -0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 422
    assert get_customer_bills("C9002") == []


def test_decreasing_meter_reading_is_not_saved():
    customer_id = f"C{uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "previous_reading": 1250,
        "current_reading": 1000,
        "unit_rate": 0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 400
    assert get_customer_bills("C9003") == []


def test_multiple_bills_for_same_customer():
    customer_id = f"C{uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    first_response = requests.post(
        f"{BASE_URL}/bills", json=payload
    )

    second_payload = {
        **payload,
        "previous_reading": 1250,
        "current_reading": 1500
    }

    second_response = requests.post(
        f"{BASE_URL}/bills", json=second_payload
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    records = get_customer_bills("C9004")

    assert len(records) == 2
    assert records[0]["total_bill"] == "62.50"
    assert records[1]["total_bill"] == "62.50"


def test_zero_consumption_bill():
    customer_id = f"C{uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "previous_reading": 1000,
        "current_reading": 1000,
        "unit_rate": 0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills", json=payload
    )

    assert response.status_code == 201
    assert response.json()["consumption_kwh"] == 0
    assert response.json()["total_bill"] == "0.00"

    database_data = get_bill(response.json()["bill_id"])

    assert database_data["consumption"] == 0
    assert database_data["total_bill"] == "0.00"