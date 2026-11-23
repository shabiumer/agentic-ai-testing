
from src.customer import Customer
from src.meter import Meter
from src.energy_bill import EnergyBill


# Create customer
customer = Customer(
    "C1001",
    "John Smith",
    "Newport"
)

# Create meter
meter = Meter("M1001")

meter.add_reading(1000)
meter.add_reading(1250)

# Generate bill
bill = EnergyBill(
    customer,
    meter,
    0.25
)

print("ENERGY BILL")
print("--------------------")

print(bill.generate_bill())
