def calculate_transport_emissions(distance_km: float, mode: str) -> float:
    """
    Calculate carbon footprint for transportation.
    
    Args:
        distance_km: The distance traveled in kilometers.
        mode: The mode of transportation (e.g., 'petrol car', 'diesel car', 'ev', 'bus', 'flight').
        
    Returns:
        float: Carbon emissions in kg CO2e.
    """
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")
        
    mode = mode.lower().strip()
    
    # Emission factors in kg CO2e per km
    factors = {
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
    
    # Default to petrol car if mode is unknown but transport is implied
    factor = factors.get(mode, 0.19)
    
    return round(distance_km * factor, 2)


def calculate_electricity_emissions(hours: float, appliance: str) -> float:
    """
    Calculate carbon footprint for electricity usage based on hours used.
    
    Args:
        hours: Number of hours the appliance was used.
        appliance: The type of appliance (e.g., 'ac', 'heater', 'laptop').
        
    Returns:
        float: Carbon emissions in kg CO2e.
    """
    if hours < 0:
        raise ValueError("Hours cannot be negative.")
        
    appliance = appliance.lower().strip()
    
    # Emission factors in kg CO2e per hour of usage (estimates)
    factors = {
        'ac': 0.80,          # Air conditioner
        'heater': 1.20,      # Room heater
        'laptop': 0.05,      # Laptop charging/usage
        'desktop': 0.15,     # Desktop computer
        'tv': 0.10           # Television
    }
    
    # Default factor if unknown
    factor = factors.get(appliance, 0.20)
    
    return round(hours * factor, 2)


def get_daily_baseline() -> float:
    """
    Returns the standard daily baseline carbon footprint in kg CO2e 
    for an average individual to compare against.
    
    Returns:
        float: Baseline daily emissions (e.g., 13.0 kg CO2e).
    """
    return 13.0
