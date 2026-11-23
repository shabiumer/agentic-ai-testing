
def analyse_usage(readings):

    # Check that readings are provided
    if not readings:
        raise ValueError("At least one reading is required")

    # Initialise total
    total = 0

    # Loop through each meter reading
    for reading in readings:

        if reading < 0:
            raise ValueError("Reading cannot be negative")

        total = total + reading

    # Calculate average
    average = total / len(readings)

    # Classify average consumption
    if average <= 100:
        category = "Low"
    elif average <= 300:
        category = "Medium"
    else:
        category = "High"

    # Return results
    return {
        "total": total,
        "average": average,
        "category": category
    }
