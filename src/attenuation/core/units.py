from __future__ import annotations
import numpy as np
import pint
from typing import Any, Optional

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# Canonical units
U_CANON = {
    "frequency": ureg.hertz,
    "angle": ureg.degree,
    "temperature": ureg.kelvin,
    "pressure": ureg.kilopascal,
}

def _as_pint(x: Any, unit: pint.Unit | str) -> Q_:
    # Accept Pint, numpy arrays, python lists, or scalars
    try:
        if isinstance(x, Q_):
            return x.to(unit)
        if isinstance(x, (list, tuple, np.ndarray)):
            return Q_(np.asarray(x), unit)
        return Q_(x, unit)
    except:
        raise ValueError(f"Cannot convert {x} to {unit}")

def normalize_inputs(ctx: Any) -> dict[str, float | np.ndarray | None]:
    """Normalize input context to SI magnitudes.

    Converts input values found on ``ctx`` into canonical SI magnitudes using
    ``pint`` and returns plain numbers or numpy arrays. Optional inputs remain
    ``None`` when not provided.

    Args:
        ctx: An object with attributes ``frequency_hz``, ``elevation_deg``,
            ``latitude_deg``, ``longitude_deg``, and optional
            ``temperature_k`` and ``pressure_kpa``. Each value may be a
            ``pint.Quantity``, array-like, or scalar.

    Returns:
        A mapping with keys ``frequency_hz``, ``elevation_deg``,
        ``latitude_deg``, ``longitude_deg``, ``temperature_k``, and
        ``pressure_kpa`` where values are SI magnitudes as floats or numpy
        arrays. Optional fields will be ``None`` if not provided.
    """
    # Returns SI magnitudes as numpy arrays or scalars; None stays None
    out = {}
    out["frequency_hz"] = _as_pint(ctx.frequency_hz, U_CANON["frequency"]).to("Hz").magnitude
    out["elevation_deg"] = _as_pint(ctx.elevation_deg, U_CANON["angle"]).to("degree").magnitude
    out["latitude_deg"] = _as_pint(ctx.latitude_deg, U_CANON["angle"]).to("degree").magnitude
    out["longitude_deg"] = _as_pint(ctx.longitude_deg, U_CANON["angle"]).to("degree").magnitude

    def opt(x: Optional[Any], unit, to_unit: str):
        if x is None:
            return None
        return _as_pint(x, unit).to(to_unit).magnitude
    
    out["temperature_k"] = opt(ctx.temperature_k, U_CANON["temperature"], "K")
    out["pressure_kpa"] = opt(ctx.pressure_kpa, U_CANON["pressure"], "kPa")
    return out

def attach_unit(value: Any, unit: str | pint.Unit | None) -> Any:
    """Attach a unit to a magnitude if a unit is provided.

    If ``unit`` is ``None``, the input ``value`` is returned unchanged.

    Args:
        value: A magnitude (scalar or array-like) representing a unitless value.
        unit: The unit to attach. When ``None``, no change is applied.

    Returns:
        Either the original ``value`` when ``unit`` is ``None`` or a
        ``pint.Quantity`` with the given unit.
    """
    if unit is None:
        return value
    return Q_(value, unit)