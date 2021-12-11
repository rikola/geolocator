from dataclasses import dataclass


@dataclass
class Location:
    """Describes a specific location on a globe."""
    name: str
    latitude: float
    longitude: float
