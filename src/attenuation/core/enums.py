from enum import StrEnum, auto

class Polarization(StrEnum):
    # For ITU-R P.838
    HORIZONTAL = auto()
    VERTICAL = auto()
    CIRCULAR = auto()

class Hydrometer(StrEnum):
    # For ITU-R P.453
    WATER = auto()
    ICE = auto()