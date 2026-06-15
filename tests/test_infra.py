import tempfile
from decimal import Decimal
from pathlib import Path

from orcalogy.infra.parser import load_config


def test_load_config_success() -> None:
    # Arrange
    toml_content = """
    [settings]
    currency = "BRL"

    [limits]
    Food = 800.00
    Leisure = 300.50
    Transport = 200
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
        tmp.write(toml_content)
        tmp_path = tmp.name

    try:
        # Act
        config = load_config(tmp_path)

        # Assert
        assert config.currency == "BRL"
        assert config.limits["Food"] == Decimal("800.00")
        assert config.limits["Leisure"] == Decimal("300.50")
        assert config.limits["Transport"] == Decimal("200.00")
    finally:
        Path(tmp_path).unlink()


def test_load_config_missing_sections() -> None:
    toml_content = """
    [settings]
    currency = "USD"
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
        tmp.write(toml_content)
        tmp_path = tmp.name

    try:
        config = load_config(tmp_path)
        assert config.currency == "USD"
        assert config.limits == {}
    finally:
        Path(tmp_path).unlink()
