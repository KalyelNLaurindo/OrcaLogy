import tomllib
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class AppConfig:
    currency: str = "BRL"
    limits: dict[str, Decimal] = field(default_factory=dict)


def load_config(file_path: str) -> AppConfig:
    """
    Loads application configuration from a TOML file.
    All category limits are mapped to Decimal values for precision.
    """
    from pathlib import Path

    with Path(file_path).open("rb") as f:
        data = tomllib.load(f)

    settings = data.get("settings", {})
    currency = settings.get("currency", "BRL")

    limits_raw = data.get("limits", {})
    limits: dict[str, Decimal] = {}
    for k, v in limits_raw.items():
        # Ensure value is converted to Decimal with two decimal places
        limits[k] = Decimal(str(v))

    return AppConfig(currency=currency, limits=limits)
