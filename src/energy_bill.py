
from decimal import Decimal


class EnergyBill:

    def __init__(self, customer, meter, unit_rate):
        self.customer = customer
        self.meter = meter
        self.unit_rate = Decimal(str(unit_rate))

        if self.unit_rate < 0:
            raise ValueError("Unit rate cannot be negative")

    def calculate_total(self):

        consumption = self.meter.calculate_consumption()

        total = Decimal(str(consumption)) * self.unit_rate

        return total.quantize(Decimal("0.01"))

    def generate_bill(self):

        return {
            "customer": self.customer.name,
            "meter_id": self.meter.meter_id,
            "consumption": self.meter.calculate_consumption(),
            "unit_rate": str(self.unit_rate),
            "total_bill": str(self.calculate_total())
        }

