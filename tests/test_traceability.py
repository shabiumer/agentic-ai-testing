import pytest

from src.traceability import build_traceability_matrix


def sample_ai_output():
    return {
        "business_rules": [
            {
                "rule_id": "BR-001",
                "description": "Calculate energy consumption"
            },
            {
                "rule_id": "BR-002",
                "description": "Reject negative readings"
            },
            {
                "rule_id": "BR-003",
                "description": "Reject decreasing readings"
            }
        ],
        "positive_tests": [
            {
                "test_case_id": "PTC-001",
                "requirement_ids": ["BR-001"]
            }
        ],
        "negative_tests": [
            {
                "test_case_id": "NTC-001",
                "requirement_ids": ["BR-002"]
            }
        ],
        "boundary_tests": [
            {
                "test_case_id": "BTC-001",
                "requirement_ids": ["BR-001", "BR-003"]
            }
        ]
    }


def test_all_requirements_are_covered():

    result = build_traceability_matrix(sample_ai_output())

    assert result["BR-001"]["coverage"] == "Covered"
    assert result["BR-002"]["coverage"] == "Covered"
    assert result["BR-003"]["coverage"] == "Covered"


def test_requirement_without_test_case():

    data = sample_ai_output()

    data["boundary_tests"] = []

    result = build_traceability_matrix(data)

    assert result["BR-003"]["coverage"] == "Not Covered"


def test_requirement_linked_to_multiple_tests():

    result = build_traceability_matrix(sample_ai_output())

    assert len(result["BR-001"]["test_cases"]) == 2


def test_unknown_requirement_id():

    data = sample_ai_output()

    data["positive_tests"][0]["requirement_ids"] = ["BR-999"]

    with pytest.raises(ValueError):
        build_traceability_matrix(data)