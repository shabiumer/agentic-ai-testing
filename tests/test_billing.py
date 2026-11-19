
import pytest

from src.billing import calculate_bill


def test_standard_energy_bill():

    result = calculate_bill(500, 0.25)

    assert result == 125.00


def test_zero_consumption():

    result = calculate_bill(0, 0.25)

    assert result == 0.00


def test_negative_consumption():

    with pytest.raises(ValueError):
        calculate_bill(-100, 0.25)


def test_negative_unit_rate():

    with pytest.raises(ValueError):
        calculate_bill(500, -0.25)
