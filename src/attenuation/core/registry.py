from typing import Dict, Tuple, Type, Any

Key = Tuple[str, str] # (rec, version)
# _REGISTRY maps (record, version) keys to their associated class types.
_REGISTRY: Dict[Key, Type[Any]] = {}

# _ALIASES maps (record, alias_version) to the canonical (record, version) key.
# This allows version aliases to resolve to the correct registered class.
# Aliases are optional; the canonical (record, version) key is used if no alias is found.
_ALIASES: Dict[Tuple[str, str], Key] = {}

def register_class(rec: str, version: str, cls: Type[Any]) -> None:
    """Register a class for a given record and version.

    Associates the given (rec, version) with the class in the registry.

    Args:
        rec (str): The record identifier.
        version (str): The version string.
        cls (type): The class to be registered.

    Returns:
        None
    """
    _REGISTRY[(rec, version)] = cls

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
    _ALIASES[(rec, alias_version)] = (rec, target_version)

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
    key = _ALIASES.get((rec, version), (rec, version))
    cls = _REGISTRY.get(key)
    if not cls:
        raise KeyError(f"No model registered for {key}")
    return cls