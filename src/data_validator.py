
def validate_customer(customer):

    required_fields = [
        "customer_id",
        "name",
        "address",
        "meter_id",
        "previous_reading",
        "current_reading",
        "unit_rate"
    ]

    for field in required_fields:

        if field not in customer:
            raise ValueError(f"Missing required field: {field}")

    for field in ["customer_id", "name", "address", "meter_id"]:

        if not isinstance(customer[field], str) or not customer[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    previous = customer["previous_reading"]
    current = customer["current_reading"]
    rate = customer["unit_rate"]

    if isinstance(previous, bool) or not isinstance(previous, int) or previous < 0:
        raise ValueError("Previous reading must be a non-negative integer")

    if isinstance(current, bool) or not isinstance(current, int) or current < 0:
        raise ValueError("Current reading must be a non-negative integer")

    if current < previous:
        raise ValueError("Current reading cannot be lower than previous reading")

    if isinstance(rate, bool) or not isinstance(rate, (int, float)) or rate < 0:
        raise ValueError("Unit rate must be a non-negative number")

    return True
