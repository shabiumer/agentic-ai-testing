import requests

BASE_URL = "http://127.0.0.1:8000"


def test_health_check():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_valid_bill():
    payload = {
        "customer_id": "C1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["consumption_kwh"] == 250
    assert response.json()["total_bill"] == "62.50"


def test_current_reading_lower_than_previous():
    payload = {
        "customer_id": "C1001",
        "previous_reading": 1250,
        "current_reading": 1000,
        "unit_rate": 0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 400


def test_negative_unit_rate():
    payload = {
        "customer_id": "C1001",
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": -0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 422


def test_missing_customer_id():
    payload = {
        "previous_reading": 1000,
        "current_reading": 1250,
        "unit_rate": 0.25
    }

    response = requests.post(
        f"{BASE_URL}/bills",
        json=payload
    )

    assert response.status_code == 422


def test_unknown_endpoint():
    response = requests.get(f"{BASE_URL}/unknown")

    assert response.status_code == 404