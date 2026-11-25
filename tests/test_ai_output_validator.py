import pytest

from src.ai_output_validator import (
    validate_test_case,
    validate_ai_output
)


def test_valid_test_case():

    test_case = {
        "test_case_id": "PTC-001",
        "test_scenario": "Calculate standard energy bill",
        "test_type": "Positive",
        "test_input": {
            "previous_reading": 1000,
            "current_reading": 1250,
            "unit_rate": 0.20
        },
        "expected_result": "50.00"
    }

    assert validate_test_case(test_case) is True


def test_missing_test_case_id():

    test_case = {
        "test_scenario": "Calculate standard energy bill",
        "test_type": "Positive",
        "test_input": {},
        "expected_result": "50.00"
    }

    with pytest.raises(ValueError):
        validate_test_case(test_case)


def test_invalid_test_type():

    test_case = {
        "test_case_id": "TC-001",
        "test_scenario": "Calculate bill",
        "test_type": "Unknown",
        "test_input": {},
        "expected_result": "50.00"
    }

    with pytest.raises(ValueError):
        validate_test_case(test_case)