import pytest
from calculations import calculate_transport_emissions, calculate_electricity_emissions, get_daily_baseline

def test_calculate_transport_emissions_petrol():
    assert calculate_transport_emissions(10, 'petrol car') == 1.90
    assert calculate_transport_emissions(20.5, 'petrol car') == 3.89

def test_calculate_transport_emissions_ev():
    assert calculate_transport_emissions(10, 'ev') == 0.50
    assert calculate_transport_emissions(10, 'electric car') == 0.50

def test_calculate_transport_emissions_unknown():
    # Should default to petrol car (0.19 factor)
    assert calculate_transport_emissions(10, 'spaceship') == 1.90

def test_calculate_transport_emissions_negative():
    with pytest.raises(ValueError):
        calculate_transport_emissions(-5, 'bus')

def test_calculate_electricity_emissions_ac():
    assert calculate_electricity_emissions(8, 'ac') == 6.40
    assert calculate_electricity_emissions(2.5, 'ac') == 2.00

def test_calculate_electricity_emissions_laptop():
    assert calculate_electricity_emissions(10, 'laptop') == 0.50

def test_calculate_electricity_emissions_unknown():
    # Should default to 0.20 factor
    assert calculate_electricity_emissions(10, 'microwave') == 2.00

def test_calculate_electricity_emissions_negative():
    with pytest.raises(ValueError):
        calculate_electricity_emissions(-2, 'tv')

def test_get_daily_baseline():
    assert get_daily_baseline() == 13.0
