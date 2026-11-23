
import pytest

from src.usage_analysis import analyse_usage


def test_normal_meter_readings():
    result = analyse_usage([100, 150, 200])

    assert result["total"] == 450
    assert result["average"] == 150
    assert result["category"] == "Medium"


def test_low_consumption():
    result = analyse_usage([50, 80, 100])

    assert result["category"] == "Low"


def test_high_consumption():
    result = analyse_usage([400, 500, 600])

    assert result["category"] == "High"


def test_negative_reading():
    with pytest.raises(ValueError):
        analyse_usage([100, -50, 200])


def test_empty_readings():
    with pytest.raises(ValueError):
        analyse_usage([])
