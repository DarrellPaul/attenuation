from typing import Dict, Tuple, Type, Any
import re

Key = Tuple[str, str] # (rec, version)
# _REGISTRY maps (record, version) keys to their associated class types.
_REGISTRY: Dict[Key, Type[Any]] = {}

# _ALIASES maps (record, alias_version) to the canonical (record, version) key.
# This allows version aliases to resolve to the correct registered class.
# Aliases are optional; the canonical (record, version) key is used if no alias is found.
_ALIASES: Dict[Tuple[str, str], Key] = {}

def _normalize_rec(rec: str) -> str:
    """Normalize and validate recommendation string to 'P.<digits>'.

    Accepts 'p.840', 'P.840', 'P840', or 'p840' and normalizes to 'P.840'.
    Raises a ValueError for any other format.

    Args:
        rec (str): The recommendation string to normalize.

    Returns:
        str: The normalized recommendation string in 'P.<digits>' form.

    Raises:
        ValueError: If the string is not a valid recommendation identifier.
    """
    text = rec.strip()
    match = re.fullmatch(r"[Pp]\.?(\d+)", text)
    if not match:
        raise ValueError(
            (
                f"Invalid recommendation string '{rec}'. "
                "Expected 'P.<digits>' (case-insensitive). "
                "Forms like 'P<digits>' will be normalized to 'P.<digits>'."
            )
        )
    return f"P.{match.group(1)}"

def register_class(rec: str, version: str, cls: Type[Any]) -> None:
    """Register a class for a given record and version.

    Associates the given (rec, version) with the class in the registry. The
    recommendation identifier ``rec`` is validated and normalized to the form
    'P.<digits>' (case-insensitive). Inputs like 'P840' or 'p840' are accepted
    and normalized to 'P.840'.

    Args:
        rec (str): The record identifier.
        version (str): The version string.
        cls (type): The class to be registered.

    Returns:
        None
    """
    rec_norm = _normalize_rec(rec)
    _REGISTRY[(rec_norm, version)] = cls

def alias(rec: str, alias_version: str, target_version: str) -> None:
    """Register an alias for a record version.

    Associates the given (rec, alias_version) with the (rec, target_version)
    in the alias registry. This allows lookups for the alias version to resolve
    to the target version.

    Args:
        rec (str): The record identifier.
        alias_version (str): The version string to be aliased.
        target_version (str): The version string to which the alias points.

    Returns:
        None
    """
    rec_norm = _normalize_rec(rec)
    _ALIASES[(rec_norm, alias_version)] = (rec_norm, target_version)

def resolve(rec: str, version: str) -> type:
    """Resolve and return the registered class for a given record and version.

    Looks up the class registered for the given record and version, following
    any aliases if present.

    Args:
        rec (str): The record identifier.
        version (str): The version string.

    Returns:
        type: The registered class associated with the record and version.

    Raises:
        KeyError: If no class is registered for the given record and version.
    """
    rec_norm = _normalize_rec(rec)
    key = _ALIASES.get((rec_norm, version), (rec_norm, version))
    cls = _REGISTRY.get(key)
    if not cls:
        raise KeyError(f"No model registered for {key}")
    return cls