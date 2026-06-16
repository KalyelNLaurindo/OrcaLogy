import datetime
import tempfile
from decimal import Decimal
from pathlib import Path

import pytest

from orcalogy.domain.models import Money
from orcalogy.infra.parser import load_config, parse_journal_file, parse_journal_lines


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


def test_advisory_file_locking(tmp_path: Path) -> None:
    """Verify that FileLockManager prevents concurrent locking on the same resource."""
    import time
    from concurrent.futures import ThreadPoolExecutor

    from filelock import Timeout

    from orcalogy.infra.locker import FileLockManager

    lock_file = tmp_path / "ledger.lock"

    # 1. Verify exclusive acquisition
    lock1 = FileLockManager(str(lock_file), timeout=0.1)
    lock2 = FileLockManager(str(lock_file), timeout=0.1)

    with lock1:
        # lock1 holds the lock, lock2 should fail due to timeout
        with pytest.raises(Timeout):
            with lock2:
                pass

    # 2. Verify release allows subsequent acquisition
    with lock2:
        pass  # should succeed now that lock1 released it

    # 3. Verify thread-safety/queuing order
    shared_resource: list[int] = []

    def worker(worker_id: int, delay: float) -> None:
        lock = FileLockManager(str(lock_file), timeout=2.0)
        with lock:
            time.sleep(delay)
            shared_resource.append(worker_id)

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Worker 1 starts and holds lock for 0.2s
        f1 = executor.submit(worker, 1, 0.2)
        # Worker 2 tries to enter shortly after, must block and wait
        time.sleep(0.05)
        f2 = executor.submit(worker, 2, 0.01)

        f1.result()
        f2.result()

    # Worker 1 must have executed and appended first
    assert shared_resource == [1, 2]


# ---------------------------------------------------------------------------
# TSK-21 — Cycle 1: Parsing valid journal lines
# ---------------------------------------------------------------------------


def test_parse_valid_single_transaction() -> None:
    lines = ["2026-06-15 | Alimentação | 25.50 | Supermercado da Esquina | #mercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 1
    assert len(result.warnings) == 0

    tx = result.transactions[0]
    assert tx.date == datetime.date(2026, 6, 15)
    assert tx.category == "Alimentação"
    assert tx.amount == Money("25.50")
    assert tx.description == "Supermercado da Esquina"
    assert tx.tags == ["#mercado"]
    assert tx.tx_id.startswith("tx_")
    assert len(tx.tx_id) == 11


def test_parse_valid_multiple_transactions() -> None:
    lines = [
        "2026-06-15 | Alimentação | 25.50 | Supermercado | #mercado",
        "2026-06-16 | Lazer | 120.00 | Cinema | #entretenimento",
    ]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 2
    assert len(result.warnings) == 0
    assert result.transactions[0].category == "Alimentação"
    assert result.transactions[1].category == "Lazer"


def test_parse_skips_empty_lines() -> None:
    lines = [
        "",
        "   ",
        "2026-06-15 | Alimentação | 25.50 | Supermercado | #mercado",
        "",
    ]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 1
    assert len(result.warnings) == 0


def test_parse_skips_comment_lines() -> None:
    lines = [
        "# isso é um comentário e deve ser ignorado",
        "2026-06-15 | Alimentação | 25.50 | Supermercado | #mercado",
        "# outro comentário",
    ]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 1
    assert len(result.warnings) == 0


def test_parse_tags_optional() -> None:
    lines = ["2026-06-15 | Alimentação | 25.50 | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 1
    assert result.transactions[0].tags == []


def test_parse_tags_are_parsed_correctly() -> None:
    lines = ["2026-06-16 | Lazer | 120.00 | Cinema + Jantar | #entretenimento #saida"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 1
    assert result.transactions[0].tags == ["#entretenimento", "#saida"]


def test_parse_tx_id_is_deterministic() -> None:
    line = "2026-06-15 | Alimentação | 25.50 | Supermercado | #mercado"
    result1 = parse_journal_lines([line])
    result2 = parse_journal_lines([line])

    assert result1.transactions[0].tx_id == result2.transactions[0].tx_id


# ---------------------------------------------------------------------------
# TSK-21 — Cycle 2: Syntax warnings for invalid journal lines
# ---------------------------------------------------------------------------


def test_parse_wrong_field_count_creates_warning() -> None:
    lines = ["2026-06-15 | Alimentação | 25.50"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert result.warnings[0].line_number == 1
    assert "3" in result.warnings[0].message


def test_parse_invalid_date_creates_warning() -> None:
    lines = ["15-06-2026 | Alimentação | 25.50 | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert "15-06-2026" in result.warnings[0].message


def test_parse_invalid_amount_creates_warning() -> None:
    lines = ["2026-06-15 | Alimentação | vinte reais | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert "vinte reais" in result.warnings[0].message


def test_parse_zero_amount_creates_warning() -> None:
    lines = ["2026-06-15 | Alimentação | 0.00 | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert "0.00" in result.warnings[0].message


def test_parse_negative_amount_creates_warning() -> None:
    lines = ["2026-06-15 | Alimentação | -50.00 | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1


def test_parse_empty_category_creates_warning() -> None:
    lines = ["2026-06-15 |   | 25.50 | Supermercado"]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert "Category" in result.warnings[0].message


def test_parse_empty_description_creates_warning() -> None:
    lines = ["2026-06-15 | Alimentação | 25.50 |   "]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 0
    assert len(result.warnings) == 1
    assert "Description" in result.warnings[0].message


def test_parse_mixed_valid_and_invalid_lines() -> None:
    lines = [
        "2026-06-15 | Alimentação | 25.50 | Supermercado | #mercado",
        "linha corrompida sem pipes",
        "2026-06-16 | Lazer | 120.00 | Cinema | #entretenimento",
        "2026-06-17 | Transporte | abc | Uber",
    ]
    result = parse_journal_lines(lines)

    assert len(result.transactions) == 2
    assert len(result.warnings) == 2
    assert result.warnings[0].line_number == 2
    assert result.warnings[1].line_number == 4


# ---------------------------------------------------------------------------
# TSK-21 — Cycle 3: Disk-backed journal file reading
# ---------------------------------------------------------------------------


def test_parse_journal_file_reads_valid_transactions(tmp_path: Path) -> None:
    journal = tmp_path / "ledger.journal"
    journal.write_text(
        "# Junho 2026\n"
        "2026-06-15 | Alimentação | 45.50 | Supermercado da Esquina | #mercado\n"
        "\n"
        "2026-06-16 | Lazer | 120.00 | Cinema + Jantar | #entretenimento\n",
        encoding="utf-8",
    )

    result = parse_journal_file(str(journal))

    assert len(result.transactions) == 2
    assert len(result.warnings) == 0
    assert result.transactions[0].date == datetime.date(2026, 6, 15)
    assert result.transactions[0].amount == Money("45.50")
    assert result.transactions[1].category == "Lazer"


def test_parse_journal_file_collects_warnings_for_bad_lines(tmp_path: Path) -> None:
    journal = tmp_path / "ledger.journal"
    journal.write_text(
        "2026-06-15 | Alimentação | 45.50 | Supermercado | #mercado\n"
        "linha sem formato correto\n",
        encoding="utf-8",
    )

    result = parse_journal_file(str(journal))

    assert len(result.transactions) == 1
    assert len(result.warnings) == 1
    assert result.warnings[0].line_number == 2


def test_parse_journal_file_handles_empty_file(tmp_path: Path) -> None:
    journal = tmp_path / "ledger.journal"
    journal.write_text("", encoding="utf-8")

    result = parse_journal_file(str(journal))

    assert result.transactions == []
    assert result.warnings == []


def test_parse_journal_file_handles_only_comments(tmp_path: Path) -> None:
    journal = tmp_path / "ledger.journal"
    journal.write_text(
        "# isso é um arquivo só com comentários\n"
        "# nenhuma transação aqui\n",
        encoding="utf-8",
    )

    result = parse_journal_file(str(journal))

    assert result.transactions == []
    assert result.warnings == []
