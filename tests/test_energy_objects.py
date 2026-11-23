
import pytest
from decimal import Decimal

from src.customer import Customer
from src.meter import Meter
from src.energy_bill import EnergyBill


def test_customer_creation():

    customer = Customer("C1001", "John Smith", "Newport")

    assert customer.customer_id == "C1001"
    assert customer.name == "John Smith"


def test_meter_consumption():

    meter = Meter("M1001")

    meter.add_reading(1000)
    meter.add_reading(1250)

    assert meter.calculate_consumption() == 250


def test_negative_meter_reading():

    meter = Meter("M1001")

    with pytest.raises(ValueError):
        meter.add_reading(-100)


def test_decreasing_meter_reading():

    meter = Meter("M1001")

    meter.add_reading(1000)

    with pytest.raises(ValueError):
        meter.add_reading(900)


def test_energy_bill_calculation():

    customer = Customer("C1001", "John Smith", "Newport")

    meter = Meter("M1001")
    meter.add_reading(1000)
    meter.add_reading(1250)

    bill = EnergyBill(customer, meter, 0.25)

    assert bill.calculate_total() == Decimal("62.50")


def test_bill_rejects_negative_unit_rate():

    customer = Customer("C1001", "John Smith", "Newport")
    meter = Meter("M1001")

    with pytest.raises(ValueError):
        EnergyBill(customer, meter, -0.25)
