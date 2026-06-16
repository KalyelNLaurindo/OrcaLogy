import datetime
import hashlib
import tomllib
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from orcalogy.domain.models import Money, Transaction


@dataclass
class AppConfig:
    currency: str = "BRL"
    limits: dict[str, Decimal] = field(default_factory=dict)


@dataclass
class ParseWarning:
    """Holds a non-fatal syntax error found on a specific journal line."""

    line_number: int
    raw_line: str
    message: str


@dataclass
class ParseResult:
    """Holds the complete output of a journal parsing session."""

    transactions: list[Transaction] = field(default_factory=list)
    warnings: list[ParseWarning] = field(default_factory=list)


def load_config(file_path: str) -> AppConfig:
    """Loads application configuration from a TOML file.

    All category limits are mapped to Decimal values for precision.
    """
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


def _make_tx_id(date_str: str, category: str, amount_str: str, description: str) -> str:
    """Generate a deterministic 11-char transaction ID from its core fields."""
    raw = f"{date_str}|{category}|{amount_str}|{description}"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8]
    return f"tx_{digest}"


def _parse_line(
    raw_line: str, line_number: int
) -> tuple[Transaction | None, ParseWarning | None]:
    """Parse a single pipe-delimited journal line into a Transaction or a ParseWarning."""
    parts = [p.strip() for p in raw_line.split("|")]

    if len(parts) < 4 or len(parts) > 5:
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message=f"Expected 4 or 5 pipe-separated fields, got {len(parts)}.",
        )

    date_str, category, amount_str, description = (
        parts[0],
        parts[1],
        parts[2],
        parts[3],
    )
    tags_str = parts[4] if len(parts) == 5 else ""

    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError:
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message=f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.",
        )

    if not category:
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message="Category field is empty.",
        )

    try:
        money = Money(amount_str)
    except (ValueError, TypeError):
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message=f"Invalid amount '{amount_str}'. Must be a positive decimal number.",
        )

    if money <= Money("0.00"):
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message=f"Amount must be positive, got '{amount_str}'.",
        )

    if not description:
        return None, ParseWarning(
            line_number=line_number,
            raw_line=raw_line,
            message="Description field is empty.",
        )

    tags = [t for t in tags_str.split() if t.startswith("#")] if tags_str else []
    tx_id = _make_tx_id(date_str, category, amount_str, description)

    transaction = Transaction(
        tx_id=tx_id,
        date=date,
        category=category,
        amount=money,
        description=description,
        tags=tags,
    )
    return transaction, None


def parse_journal_lines(lines: list[str]) -> ParseResult:
    """Parse a list of raw journal text lines into transactions and warnings.

    Skips blank lines and lines starting with '#'. Non-fatal errors are
    collected as ParseWarning entries instead of aborting the whole parse.
    """
    result = ParseResult()

    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        transaction, warning = _parse_line(stripped, line_number)

        if transaction is not None:
            result.transactions.append(transaction)
        if warning is not None:
            result.warnings.append(warning)

    return result


def parse_journal_file(file_path: str) -> ParseResult:
    """Read a journal file from disk and parse its lines into transactions.

    Uses UTF-8 encoding to support non-ASCII category names and descriptions.
    """
    lines = Path(file_path).read_text(encoding="utf-8").splitlines()
    return parse_journal_lines(lines)
