
class Meter:

    def __init__(self, meter_id):
        self.meter_id = meter_id
        self.readings = []

    def add_reading(self, reading):

        if reading < 0:
            raise ValueError("Meter reading cannot be negative")

        if self.readings and reading < self.readings[-1]:
            raise ValueError("New meter reading cannot be lower than previous reading")

        self.readings.append(reading)

    def calculate_consumption(self):

        if len(self.readings) < 2:
            raise ValueError("At least two readings are required")

        return self.readings[-1] - self.readings[0]


