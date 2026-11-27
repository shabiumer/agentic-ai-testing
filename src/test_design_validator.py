
def validate_designed_test_cases(output, valid_requirement_ids):
    required_fields = [
        "test_case_id",
        "test_scenario",
        "test_type",
        "requirement_ids",
        "priority",
        "test_input",
        "test_steps",
        "expected_result"
    ]

    test_cases = output.get("test_cases", [])
    issues = []
    test_ids = []

    if not test_cases:
        issues.append("No test cases generated")

    for test_case in test_cases:
        test_id = test_case.get("test_case_id", "Unknown")

        # Check required fields
        for field in required_fields:
            if field not in test_case:
                issues.append(f"{test_id}: Missing field {field}")

        if any(field not in test_case for field in required_fields):
            continue

        # Check unique IDs
        if test_id in test_ids:
            issues.append(f"{test_id}: Duplicate test case ID")
        test_ids.append(test_id)

        # Check test type
        if test_case["test_type"] not in [
            "Positive", "Negative", "Boundary"
        ]:
            issues.append(f"{test_id}: Invalid test type")

        # Check priority
        if test_case["priority"] not in ["High", "Medium", "Low"]:
            issues.append(f"{test_id}: Invalid priority")

        # Check requirement links
        if not test_case["requirement_ids"]:
            issues.append(f"{test_id}: No requirement links")

        for requirement_id in test_case["requirement_ids"]:
            if requirement_id not in valid_requirement_ids:
                issues.append(
                    f"{test_id}: Unknown requirement {requirement_id}"
                )

        # Check test input, steps and expected result
        if not test_case["test_input"]:
            issues.append(f"{test_id}: Empty test input")

        if not test_case["test_steps"]:
            issues.append(f"{test_id}: No test steps")

        if not test_case["expected_result"].strip():
            issues.append(f"{test_id}: Empty expected result")

        # Check for conditional expected results
        conditional_phrases = [
            "provided",
            "assuming",
            "depending on",
            "subject to",
            "if permitted",
            "if allowed",
            "if accepted",
            "unless"
        ]

        expected_result = test_case["expected_result"].lower()

        if any(
            phrase in expected_result
            for phrase in conditional_phrases
        ):
            issues.append(
                f"{test_id}: Expected result contains conditional "
                "behaviour that requires requirement clarification"
            )

    return {
        "status": "Passed" if not issues else "Rejected",
        "total_test_cases": len(test_cases),
        "issues": issues
    }
