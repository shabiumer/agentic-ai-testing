
from src.customer import Customer
from src.meter import Meter
from src.energy_bill import EnergyBill
from src.data_loader import load_customer_data
from src.data_validator import validate_customer


def run_billing():

    data = load_customer_data()

    for record in data["customers"]:

        validate_customer(record)

        customer = Customer(
            record["customer_id"],
            record["name"],
            record["address"]
        )

        meter = Meter(record["meter_id"])

        meter.add_reading(record["previous_reading"])
        meter.add_reading(record["current_reading"])

        bill = EnergyBill(
            customer,
            meter,
            record["unit_rate"]
        )

        print(bill.generate_bill())


if __name__ == "__main__":
    run_billing()
