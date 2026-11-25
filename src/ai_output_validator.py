def validate_test_case(test_case):

    required_fields = [
        "test_case_id",
        "test_scenario",
        "test_type",
        "test_input",
        "expected_result"
    ]

    for field in required_fields:
        if field not in test_case:
            raise ValueError(f"Missing required field: {field}")

    valid_types = ["Positive", "Negative", "Boundary"]

    if test_case["test_type"] not in valid_types:
        raise ValueError("Invalid test type")

    if not test_case["test_case_id"].strip():
        raise ValueError("Test case ID cannot be empty")

    if not test_case["test_scenario"].strip():
        raise ValueError("Test scenario cannot be empty")

    return True


def validate_ai_output(ai_output):

    required_sections = [
        "business_rules",
        "positive_tests",
        "negative_tests",
        "boundary_tests",
        "unclear_requirements"
    ]

    for section in required_sections:
        if section not in ai_output:
            raise ValueError(f"Missing section: {section}")

    all_tests = (
        ai_output["positive_tests"]
        + ai_output["negative_tests"]
        + ai_output["boundary_tests"]
    )

    test_ids = []

    for test_case in all_tests:
        validate_test_case(test_case)
        test_ids.append(test_case["test_case_id"])

    if len(test_ids) != len(set(test_ids)):
        raise ValueError("Duplicate test case IDs found")

    return True