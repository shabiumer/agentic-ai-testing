
import pytest

from src.test_design_validator import validate_designed_test_cases


VALID_REQUIREMENT_IDS = ["BR-001", "BR-002"]


def create_test_case():
    return {
        "test_case_id": "TC-001",
        "test_scenario": "Reject negative meter readings",
        "test_type": "Negative",
        "requirement_ids": ["BR-002"],
        "priority": "High",
        "test_input": {
            "previous_meter_reading": -10,
            "current_meter_reading": -1,
            "unit_rate": 0.275
        },
        "test_steps": [
            "Navigate to the bill calculation screen.",
            "Enter negative meter readings.",
            "Submit the calculation request."
        ],
        "expected_result": "The system rejects the negative readings."
    }


def test_valid_test_design_output():
    output = {
        "test_cases": [create_test_case()],
        "unclear_requirements": []
    }

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Passed"
    assert result["total_test_cases"] == 1
    assert result["issues"] == []


def test_missing_expected_result():
    test_case = create_test_case()
    del test_case["expected_result"]

    output = {"test_cases": [test_case]}

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Missing field expected_result" in issue
               for issue in result["issues"])


def test_duplicate_test_case_ids():
    first_case = create_test_case()
    second_case = create_test_case()

    second_case["test_scenario"] = "Reject negative current reading"

    output = {
        "test_cases": [first_case, second_case]
    }

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Duplicate test case ID" in issue
               for issue in result["issues"])


def test_invalid_priority():
    test_case = create_test_case()
    test_case["priority"] = "Urgent"

    output = {"test_cases": [test_case]}

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Invalid priority" in issue
               for issue in result["issues"])


def test_unknown_requirement_id():
    test_case = create_test_case()
    test_case["requirement_ids"] = ["BR-999"]

    output = {"test_cases": [test_case]}

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Rejected"
    assert any("Unknown requirement BR-999" in issue
               for issue in result["issues"])

def test_conditional_expected_result():
    test_case = create_test_case()

    test_case["expected_result"] = (
        "The system calculates zero consumption, "
        "provided equal readings are accepted."
    )

    output = {
        "test_cases": [test_case],
        "unclear_requirements": [
            "Whether equal readings are accepted is unclear."
        ]
    }

    result = validate_designed_test_cases(
        output, VALID_REQUIREMENT_IDS
    )

    assert result["status"] == "Rejected"
    assert any(
        "conditional behaviour" in issue
        for issue in result["issues"]
    )