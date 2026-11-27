
from src.test_case_quality import assess_test_case_quality, calculate_quality_score
from src.test_case_quality import find_duplicate_test_cases
from src.test_case_quality import validate_requirement_links


def test_valid_requirement_link():

    test_case = {
        "requirement_ids": ["BR-001", "BR-002"]
    }

    result = validate_requirement_links(
        test_case,
        ["BR-001", "BR-002", "BR-003"]
    )

    assert result["status"] == "Passed"


def test_invalid_requirement_link():

    test_case = {
        "requirement_ids": ["BR-999"]
    }

    result = validate_requirement_links(
        test_case,
        ["BR-001", "BR-002", "BR-003"]
    )

    assert result["status"] == "Rejected"
    assert "Unknown requirement IDs: ['BR-999']" in result["issues"]


def test_duplicate_test_cases():

    test_cases = [
        {
            "test_case_id": "TC-001",
            "test_scenario": "Calculate standard bill",
            "test_input": {
                "previous_reading": 1000,
                "current_reading": 1250
            }
        },
        {
            "test_case_id": "TC-002",
            "test_scenario": "Calculate standard bill",
            "test_input": {
                "previous_reading": 1000,
                "current_reading": 1250
            }
        }
    ]

    result = find_duplicate_test_cases(test_cases)

    assert result == ["TC-002"]


def test_no_duplicate_test_cases():

    test_cases = [
        {
            "test_case_id": "TC-001",
            "test_scenario": "Calculate standard bill",
            "test_input": {"previous_reading": 1000}
        },
        {
            "test_case_id": "TC-002",
            "test_scenario": "Calculate high usage bill",
            "test_input": {"previous_reading": 2000}
        }
    ]

    result = find_duplicate_test_cases(test_cases)

    assert result == []


def test_good_test_case():

    test_case = {
        "test_case_id": "TC-POS-001",
        "test_scenario": "Calculate a standard energy bill",
        "test_type": "Positive",
        "requirement_ids": ["BR-001"],
        "test_input": {
            "previous_reading": 1000,
            "current_reading": 1250,
            "unit_rate": 0.25
        },
        "expected_result": "Bill should be 62.50"
    }

    result = assess_test_case_quality(test_case)

    assert result["status"] == "Passed"
    assert result["issues"] == []


def test_missing_expected_result():

    test_case = {
        "test_case_id": "TC-POS-002",
        "test_scenario": "Calculate an energy bill",
        "test_type": "Positive",
        "requirement_ids": ["BR-001"],
        "test_input": {"previous_reading": 1000}
    }

    result = assess_test_case_quality(test_case)

    assert result["status"] == "Rejected"
    assert "Missing field: expected_result" in result["issues"]


def test_invalid_test_type():

    test_case = {
        "test_case_id": "TC-001",
        "test_scenario": "Calculate an energy bill",
        "test_type": "Random",
        "requirement_ids": ["BR-001"],
        "test_input": {"previous_reading": 1000},
        "expected_result": "Bill calculated"
    }

    result = assess_test_case_quality(test_case)

    assert result["status"] == "Rejected"
    assert "Invalid test type" in result["issues"]

def test_quality_score():

    test_case = {
        "test_case_id": "TC-001",
        "test_scenario": "Calculate standard bill",
        "test_type": "Positive",
        "requirement_ids": ["BR-001"],
        "test_input": {"previous_reading": 1000},
        "expected_result": "Bill should be 62.50"
    }

    result = calculate_quality_score(test_case)

    assert result["score"] == 5
    assert result["percentage"] == 100