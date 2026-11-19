
from decimal import Decimal


def calculate_bill(consumption, unit_rate):

    consumption = Decimal(str(consumption))
    unit_rate = Decimal(str(unit_rate))

    if consumption < 0:
        raise ValueError("Consumption cannot be negative")

    if unit_rate < 0:
        raise ValueError("Unit rate cannot be negative")

    total = consumption * unit_rate

    return total.quantize(Decimal("0.01"))
