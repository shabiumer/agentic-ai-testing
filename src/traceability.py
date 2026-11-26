def build_traceability_matrix(ai_output):

    business_rules = ai_output["business_rules"]

    all_tests = (
        ai_output["positive_tests"]
        + ai_output["negative_tests"]
        + ai_output["boundary_tests"]
    )

    matrix = {}

    for rule in business_rules:
        rule_id = rule["rule_id"]

        matrix[rule_id] = {
            "description": rule["description"],
            "test_cases": []
        }

    for test_case in all_tests:
        for requirement_id in test_case["requirement_ids"]:

            if requirement_id not in matrix:
                raise ValueError(
                    f"Unknown requirement ID: {requirement_id}"
                )

            matrix[requirement_id]["test_cases"].append(
                test_case["test_case_id"]
            )

    for rule_id, details in matrix.items():
        details["coverage"] = (
            "Covered" if details["test_cases"] else "Not Covered"
        )

    return matrix