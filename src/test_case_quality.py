
def assess_test_case_quality(test_case):

    issues = []

    # Check 1: Required fields
    required_fields = [
        "test_case_id",
        "test_scenario",
        "test_type",
        "requirement_ids",
        "test_input",
        "expected_result"
    ]

    for field in required_fields:
        if field not in test_case:
            issues.append(f"Missing field: {field}")

    # Stop if essential fields are missing
    if issues:
        return {
            "status": "Rejected",
            "issues": issues
        }

    # Check 2: Empty test scenario
    if not test_case["test_scenario"].strip():
        issues.append("Test scenario cannot be empty")

    # Check 3: Valid test type
    valid_types = ["Positive", "Negative", "Boundary"]

    if test_case["test_type"] not in valid_types:
        issues.append("Invalid test type")

    # Check 4: Requirement IDs
    if not test_case["requirement_ids"]:
        issues.append("No requirement ID linked")

    # Check 5: Test input
    if not test_case["test_input"]:
        issues.append("Test input cannot be empty")

    # Check 6: Expected result
    if not test_case["expected_result"].strip():
        issues.append("Expected result cannot be empty")

    return {
        "status": "Passed" if not issues else "Rejected",
        "issues": issues
    }


def find_duplicate_test_cases(test_cases):

    seen = set()
    duplicates = []

    for test_case in test_cases:

        signature = (
            test_case["test_scenario"].strip().lower(),
            str(test_case["test_input"])
        )

        if signature in seen:
            duplicates.append(test_case["test_case_id"])
        else:
            seen.add(signature)

    return duplicates


def validate_requirement_links(test_case, valid_requirement_ids):

    invalid_ids = [
        requirement_id
        for requirement_id in test_case["requirement_ids"]
        if requirement_id not in valid_requirement_ids
    ]

    if invalid_ids:
        return {
            "status": "Rejected",
            "issues": [
                f"Unknown requirement IDs: {invalid_ids}"
            ]
        }

    return {
        "status": "Passed",
        "issues": []
    }

def calculate_quality_score(test_case):

    checks = [
        all(
            field in test_case
            for field in [
                "test_case_id",
                "test_scenario",
                "test_type",
                "requirement_ids",
                "test_input",
                "expected_result"
            ]
        ),
        test_case.get("test_type") in [
            "Positive", "Negative", "Boundary"
        ],
        bool(test_case.get("requirement_ids")),
        bool(test_case.get("test_input")),
        bool(test_case.get("expected_result", "").strip())
    ]

    score = sum(checks)

    return {
        "score": score,
        "maximum_score": 5,
        "percentage": score * 20
    }
