
import pytest

from src.test_data_validator import validate_test_data


VALID_TEST_CASE_IDS = ["TC-001", "TC-002"]


def create_dataset():
    return {
        "test_data_id": "TD-001",
        "test_case_id": "TC-001",
        "description": "Standard billing test data",
        "data": {
            "previous_meter_reading": 1250,
            "current_meter_reading": 1350,
            "unit_rate": 0.25
        },
        "data_type": "Positive",
        "purpose": "Verify standard bill calculation"
    }


def test_valid_test_data():
    output = {"test_data": [create_dataset()]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Passed"
    assert result["total_datasets"] == 1
    assert result["issues"] == []


def test_missing_required_field():
    dataset = create_dataset()
    del dataset["purpose"]

    output = {"test_data": [dataset]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Missing field purpose" in issue
               for issue in result["issues"])


def test_duplicate_test_data_ids():
    first = create_dataset()
    second = create_dataset()
    second["test_case_id"] = "TC-002"

    output = {"test_data": [first, second]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Duplicate test data ID" in issue
               for issue in result["issues"])


def test_unknown_test_case_id():
    dataset = create_dataset()
    dataset["test_case_id"] = "TC-999"

    output = {"test_data": [dataset]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Unknown test case ID" in issue
               for issue in result["issues"])


def test_invalid_data_type():
    dataset = create_dataset()
    dataset["data_type"] = "Random"

    output = {"test_data": [dataset]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Invalid data type" in issue
               for issue in result["issues"])



def test_positive_data_with_negative_reading_is_rejected():
    dataset = create_dataset()
    dataset["data"]["previous_meter_reading"] = -10
    dataset["data_type"] = "Positive"

    output = {"test_data": [dataset]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"


def test_negative_data_with_valid_readings_is_rejected():
    dataset = create_dataset()
    dataset["data_type"] = "Negative"

    output = {"test_data": [dataset]}

    result = validate_test_data(
        output, VALID_TEST_CASE_IDS
    )

    assert result["status"] == "Rejected"
