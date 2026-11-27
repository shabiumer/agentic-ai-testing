
def validate_test_data(output, valid_test_case_ids):
    required_fields = [
        "test_data_id",
        "test_case_id",
        "description",
        "data",
        "data_type",
        "purpose"
    ]

    test_datasets = output.get("test_data", [])
    issues = []
    test_data_ids = []

    if not test_datasets:
        issues.append("No test data generated")

    for dataset in test_datasets:
        data_id = dataset.get("test_data_id", "Unknown")

        # Check required fields
        for field in required_fields:
            if field not in dataset:
                issues.append(f"{data_id}: Missing field {field}")

        if any(field not in dataset for field in required_fields):
            continue

        # Check unique test data IDs
        if data_id in test_data_ids:
            issues.append(f"{data_id}: Duplicate test data ID")

        test_data_ids.append(data_id)

        # Check test case reference
        if dataset["test_case_id"] not in valid_test_case_ids:
            issues.append(
                f"{data_id}: Unknown test case ID "
                f"{dataset['test_case_id']}"
            )

        # Check data type
        if dataset["data_type"] not in [
            "Positive", "Negative", "Boundary"
        ]:
            issues.append(f"{data_id}: Invalid data type")

        # Check test input fields
        test_input = dataset["data"]

        input_fields = [
            "previous_meter_reading",
            "current_meter_reading",
            "unit_rate"
        ]

        for field in input_fields:
            if field not in test_input:
                issues.append(f"{data_id}: Missing input {field}")
            elif not isinstance(test_input[field], (int, float)):
                issues.append(f"{data_id}: Invalid numeric input {field}")


        # Check data against known meter-reading rules
        previous = test_input.get("previous_meter_reading")
        current = test_input.get("current_meter_reading")

        numeric_readings = (
            isinstance(previous, (int, float))
            and not isinstance(previous, bool)
            and isinstance(current, (int, float))
            and not isinstance(current, bool)
        )

        if numeric_readings:

            invalid_reading = previous < 0 or current < 0
            decreasing_reading = current < previous

            if dataset["data_type"] == "Positive":
                if invalid_reading or decreasing_reading:
                    issues.append(
                        f"{data_id}: Positive data violates meter-reading rules"
                    )

            elif dataset["data_type"] == "Negative":
                if not (invalid_reading or decreasing_reading):
                    issues.append(
                        f"{data_id}: Negative data does not violate a known meter-reading rule"
                    )

    return {
        "status": "Passed" if not issues else "Rejected",
        "total_datasets": len(test_datasets),
        "issues": issues
    }

