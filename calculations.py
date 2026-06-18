from typing import Final

# --- CONSTANTS: EMISSION FACTORS ---
# Emission factors in kg CO2e per km
TRANSPORT_FACTORS: Final[dict[str, float]] = {
    'petrol car': 0.19,
    'diesel car': 0.21,
    'ev': 0.05,
    'electric car': 0.05,
    'bus': 0.10,
    'public transport': 0.10,
    'flight': 0.15,
    'train': 0.04,
    'bike': 0.0,
    'walk': 0.0
}

# Emission factors in kg CO2e per hour of usage
ELECTRICITY_FACTORS: Final[dict[str, float]] = {
    'ac': 0.80,          # Air conditioner
    'heater': 1.20,      # Room heater
    'laptop': 0.05,      # Laptop charging/usage
    'desktop': 0.15,     # Desktop computer
    'tv': 0.10           # Television
}

DEFAULT_TRANSPORT_FACTOR: Final[float] = 0.19
DEFAULT_ELECTRICITY_FACTOR: Final[float] = 0.20
DAILY_BASELINE_KG: Final[float] = 13.0


def calculate_transport_emissions(distance_km: float, mode: str) -> float:
    """
    Calculate the carbon footprint for a transportation activity.
    
    Args:
        distance_km (float): The distance traveled in kilometers. Must be >= 0.
        mode (str): The mode of transportation (e.g., 'petrol car', 'ev', 'flight').
        
    Returns:
        float: Calculated carbon emissions in kg CO2e, rounded to 2 decimal places.
        
    Raises:
        ValueError: If distance_km is negative.
    """
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")
        
    normalized_mode: str = mode.lower().strip()
    factor: float = TRANSPORT_FACTORS.get(normalized_mode, DEFAULT_TRANSPORT_FACTOR)
    
    return round(distance_km * factor, 2)


def calculate_electricity_emissions(hours: float, appliance: str) -> float:
    """
    Calculate the carbon footprint for electricity usage based on hours used.
    
    Args:
        hours (float): Number of hours the appliance was used. Must be >= 0.
        appliance (str): The type of appliance (e.g., 'ac', 'laptop').
        
    Returns:
        float: Calculated carbon emissions in kg CO2e, rounded to 2 decimal places.
        
    Raises:
        ValueError: If hours is negative.
    """
    if hours < 0:
        raise ValueError("Hours cannot be negative.")
        
    normalized_appliance: str = appliance.lower().strip()
    factor: float = ELECTRICITY_FACTORS.get(normalized_appliance, DEFAULT_ELECTRICITY_FACTOR)
    
    return round(hours * factor, 2)


def get_daily_baseline() -> float:
    """
    Retrieve the standard daily baseline carbon footprint for an average individual.
    
    Returns:
        float: Baseline daily emissions in kg CO2e.
    """
    return DAILY_BASELINE_KG
