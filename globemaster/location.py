from dataclasses import dataclass


@dataclass
class Location:
    """Describes a specific location on a globe."""
    id: int
    name: str
    latitude: float
    longitude: float
