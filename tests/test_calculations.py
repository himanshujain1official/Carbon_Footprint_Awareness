import pytest
from calculations import (
    calculate_transport_emissions,
    calculate_electricity_emissions,
    get_daily_baseline,
    TRANSPORT_FACTORS,
    ELECTRICITY_FACTORS,
    DEFAULT_TRANSPORT_FACTOR,
    DEFAULT_ELECTRICITY_FACTOR,
    DAILY_BASELINE_KG
)

class TestCalculations:
    
    @pytest.mark.parametrize("distance, mode, expected", [
        # Valid known modes
        (10.0, "petrol car", round(10.0 * TRANSPORT_FACTORS['petrol car'], 2)),
        (20.5, "ev", round(20.5 * TRANSPORT_FACTORS['ev'], 2)),
        (15.0, "bus", round(15.0 * TRANSPORT_FACTORS['bus'], 2)),
        (5.0, "walk", 0.0),
        # Case insensitivity & whitespace
        (10.0, " Petrol Car ", round(10.0 * TRANSPORT_FACTORS['petrol car'], 2)),
        # Fallback for unknown modes
        (10.0, "spaceship", round(10.0 * DEFAULT_TRANSPORT_FACTOR, 2)),
        # Zero distance
        (0.0, "petrol car", 0.0),
        # Extremely large floats
        (1e6, "ev", round(1e6 * TRANSPORT_FACTORS['ev'], 2)),
    ])
    def test_calculate_transport_emissions_valid(self, distance: float, mode: str, expected: float) -> None:
        """Test transport calculations with various valid, edge, and fallback inputs."""
        assert calculate_transport_emissions(distance, mode) == expected

    @pytest.mark.parametrize("distance, mode", [
        (-1.0, "petrol car"),
        (-50.5, "ev")
    ])
    def test_calculate_transport_emissions_negative(self, distance: float, mode: str) -> None:
        """Test that negative distances correctly raise a ValueError."""
        with pytest.raises(ValueError, match="Distance cannot be negative."):
            calculate_transport_emissions(distance, mode)

    @pytest.mark.parametrize("hours, appliance, expected", [
        # Valid known appliances
        (2.0, "ac", round(2.0 * ELECTRICITY_FACTORS['ac'], 2)),
        (5.5, "laptop", round(5.5 * ELECTRICITY_FACTORS['laptop'], 2)),
        # Case insensitivity & whitespace
        (3.0, " AC ", round(3.0 * ELECTRICITY_FACTORS['ac'], 2)),
        # Fallback for unknown appliances
        (4.0, "quantum computer", round(4.0 * DEFAULT_ELECTRICITY_FACTOR, 2)),
        # Zero hours
        (0.0, "heater", 0.0),
        # Extremely large floats
        (1e5, "tv", round(1e5 * ELECTRICITY_FACTORS['tv'], 2)),
    ])
    def test_calculate_electricity_emissions_valid(self, hours: float, appliance: str, expected: float) -> None:
        """Test electricity calculations with various valid, edge, and fallback inputs."""
        assert calculate_electricity_emissions(hours, appliance) == expected

    @pytest.mark.parametrize("hours, appliance", [
        (-1.0, "ac"),
        (-24.0, "tv")
    ])
    def test_calculate_electricity_emissions_negative(self, hours: float, appliance: str) -> None:
        """Test that negative hours correctly raise a ValueError."""
        with pytest.raises(ValueError, match="Hours cannot be negative."):
            calculate_electricity_emissions(hours, appliance)

    def test_get_daily_baseline(self) -> None:
        """Test that the daily baseline returns the correct constant."""
        assert get_daily_baseline() == DAILY_BASELINE_KG
