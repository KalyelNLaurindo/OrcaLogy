"""Tests for the Typer CLI root controller and all CLI commands.

Covers base commands (help, version), init, add, and report subcommands.
"""

import datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from orcalogy.app.services import InitializeBudgetUseCase, RegisterTransactionUseCase
from orcalogy.cli.commands import VERSION, app
from orcalogy.domain.models import Money, Transaction
from orcalogy.infra.file_repo import FileLedgerRepository

runner = CliRunner()


# ---------------------------------------------------------------------------
# Base CLI
# ---------------------------------------------------------------------------


class TestCliBaseCommands:
    """Group: base CLI setup — help, version, and error handling."""

    def test_help_flag_returns_exit_zero(self) -> None:
        """Invoking --help should succeed without any errors."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

    def test_help_output_contains_program_name(self) -> None:
        """Help text must reference the CLI name so users recognise the tool."""
        result = runner.invoke(app, ["--help"])
        assert "orca" in result.output.lower()

    def test_help_output_contains_version_option(self) -> None:
        """Help text must advertise --version so users can check what is installed."""
        result = runner.invoke(app, ["--help"])
        assert "--version" in result.output

    def test_version_flag_returns_version_string(self) -> None:
        """--version must print the current package version and exit cleanly."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert VERSION in result.output

    def test_version_short_flag_returns_version_string(self) -> None:
        """-V must print the current package version and exit cleanly."""
        result = runner.invoke(app, ["-V"])
        assert result.exit_code == 0
        assert VERSION in result.output

    def test_unknown_command_returns_nonzero_exit(self) -> None:
        """An unrecognized subcommand must be rejected with a non-zero exit code."""
        result = runner.invoke(app, ["nonexistent-command"])
        assert result.exit_code != 0

    def test_default_without_args_runs_tui(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Invoking orca without arguments should boot the TUI app."""
        from unittest.mock import MagicMock
        mock_app = MagicMock()
        monkeypatch.setattr("orcalogy.cli.commands.OrcaLogyApp", mock_app)
        
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        mock_app.return_value.run.assert_called_once()



# ---------------------------------------------------------------------------
# orca init
# ---------------------------------------------------------------------------


class TestInitCommand:
    """Group: orca init — interactive monthly budget creation."""

    def test_init_creates_budget_with_categories(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Running init with valid input should persist the budget and categories."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["init"], input="2026-06\nAlimentação\n500\n\n")
        assert result.exit_code == 0
        budget = tmp_repo.get_budget("2026-06")
        assert budget is not None
        assert "Alimentação" in budget.categories

    def test_init_rejects_duplicate_month(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Running init twice for the same month must fail with a non-zero exit."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        runner.invoke(app, ["init"], input="2026-06\nAlimentação\n500\n\n")
        result = runner.invoke(app, ["init"], input="2026-06\nTransporte\n200\n\n")
        assert result.exit_code != 0

    def test_init_requires_at_least_one_category(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Submitting no categories must abort with an error message."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["init"], input="2026-06\n\n")
        assert result.exit_code != 0
        assert "categoria" in result.output.lower()


# ---------------------------------------------------------------------------
# orca add
# ---------------------------------------------------------------------------


class TestAddCommand:
    """Group: orca add — transaction registration with overrun confirmation."""

    def _setup_budget(self, repo: FileLedgerRepository, month: str = "2026-06") -> None:
        """Create a minimal budget with a single 100 CAD category for testing."""
        InitializeBudgetUseCase(repo).execute(month, {"Alimentação": Money("100")})

    def test_add_registers_valid_transaction(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A transaction within the category limit should be saved without prompts."""
        self._setup_budget(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "50.00",
                "--description",
                "Mercado",
                "--date",
                "2026-06-16",
            ],
        )
        assert result.exit_code == 0
        assert "registrada" in result.output.lower()

    def test_add_shows_overrun_warning_and_aborts_on_n(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Overrun + 'n' confirmation must cancel without persisting the transaction."""
        self._setup_budget(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "150.00",
                "--description",
                "Mercado",
                "--date",
                "2026-06-16",
            ],
            input="n\n",
        )
        assert result.exit_code == 0
        assert "cancelada" in result.output.lower()
        budget = tmp_repo.get_budget("2026-06")
        assert budget is not None
        assert len(budget.transactions) == 0

    def test_add_shows_overrun_warning_and_forces_on_y(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Overrun + 'y' confirmation must persist the transaction with force=True."""
        self._setup_budget(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "150.00",
                "--description",
                "Mercado",
                "--date",
                "2026-06-16",
            ],
            input="y\n",
        )
        assert result.exit_code == 0
        assert "registrada" in result.output.lower()
        budget = tmp_repo.get_budget("2026-06")
        assert budget is not None
        assert len(budget.transactions) == 1

    def test_add_rejects_invalid_date_format(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A date string not matching YYYY-MM-DD must cause a non-zero exit."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "50",
                "--description",
                "x",
                "--date",
                "16-06-2026",
            ],
        )
        assert result.exit_code != 0

    def test_add_rejects_invalid_amount(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A non-numeric amount must cause a non-zero exit."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "abc",
                "--description",
                "x",
                "--date",
                "2026-06-16",
            ],
        )
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# orca report
# ---------------------------------------------------------------------------


class TestReportCommand:
    """Group: orca report — ANSI color-coded deviation table."""

    def _setup_budget_with_transactions(self, repo: FileLedgerRepository) -> None:
        """Create a budget with one overrun category and one under-limit category."""
        InitializeBudgetUseCase(repo).execute(
            "2026-06",
            {"Alimentação": Money("100"), "Transporte": Money("200")},
        )
        # Alimentação: 150 spent / 100 limit → +50% overrun
        RegisterTransactionUseCase(repo).execute(
            Transaction(
                tx_id="tx-1",
                date=datetime.date(2026, 6, 16),
                category="Alimentação",
                amount=Money("150"),
                description="Mercado",
            ),
            force=True,
        )
        # Transporte: 50 spent / 200 limit → -75% under
        RegisterTransactionUseCase(repo).execute(
            Transaction(
                tx_id="tx-2",
                date=datetime.date(2026, 6, 16),
                category="Transporte",
                amount=Money("50"),
                description="Uber",
            ),
        )

    def test_report_renders_table_headers(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Output must contain column headers for all key fields."""
        self._setup_budget_with_transactions(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["report", "--month", "2026-06"])
        assert result.exit_code == 0
        assert "Categoria" in result.output
        assert "Limite" in result.output
        assert "Desvio" in result.output

    def test_report_green_for_under_limit(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """An under-limit category must show a negative deviation in the output."""
        self._setup_budget_with_transactions(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["report", "--month", "2026-06"])
        assert result.exit_code == 0
        # Transporte: 50 spent / 200 limit → -75.00% (under limit → green row)
        assert "-75.00%" in result.output

    def test_report_red_for_overrun(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """An overrun category must show a positive deviation in the output."""
        self._setup_budget_with_transactions(tmp_repo)
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["report", "--month", "2026-06"])
        assert result.exit_code == 0
        # Alimentação: 150 spent / 100 limit → +50.00% (overrun → red row)
        assert "+50.00%" in result.output

    def test_report_fails_for_unknown_month(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Requesting a report for a month with no budget must exit non-zero."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["report", "--month", "2099-12"])
        assert result.exit_code != 0
        assert "não encontrado" in result.output


# ---------------------------------------------------------------------------
# orca close
# ---------------------------------------------------------------------------


class TestCloseCommand:
    """Group: orca close — lock budget cycle for a specific month."""

    def test_close_locks_budget_successfully(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Closing a valid open budget must succeed, lock it, and print confirmation."""
        InitializeBudgetUseCase(tmp_repo).execute(
            "2026-06", {"Alimentação": Money("100")}
        )
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)

        result = runner.invoke(app, ["close", "--month", "2026-06"])
        assert result.exit_code == 0
        assert "fechado" in result.output.lower()

        # Subsequent add must fail because budget is locked
        add_result = runner.invoke(
            app,
            [
                "add",
                "--category",
                "Alimentação",
                "--amount",
                "50.00",
                "--description",
                "Almoço",
                "--date",
                "2026-06-17",
            ],
        )
        assert add_result.exit_code != 0
        assert "fechado" in add_result.output.lower()

    def test_close_fails_for_nonexistent_month(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Closing a month that has no initialized budget must fail."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["close", "--month", "2026-07"])
        assert result.exit_code != 0
        assert "não encontrado" in result.output.lower()

    def test_close_fails_for_already_closed_month(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Closing an already locked budget cycle must fail with appropriate message."""
        InitializeBudgetUseCase(tmp_repo).execute(
            "2026-06", {"Alimentação": Money("100")}
        )
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)

        # Close once
        runner.invoke(app, ["close", "--month", "2026-06"])

        # Close twice
        result = runner.invoke(app, ["close", "--month", "2026-06"])
        assert result.exit_code != 0
        assert "já" in result.output.lower()


# ---------------------------------------------------------------------------
# orca status
# ---------------------------------------------------------------------------


class TestStatusCommand:
    """Group: orca status — lightweight overview of the budget period."""

    def test_status_shows_correct_totals_and_state(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Status command must report totals, remaining budget, state, and overruns."""
        InitializeBudgetUseCase(tmp_repo).execute(
            "2026-06",
            {"Alimentação": Money("100"), "Transporte": Money("200")},
        )
        # Category 1 overrun (+50)
        RegisterTransactionUseCase(tmp_repo).execute(
            Transaction(
                tx_id="tx-1",
                date=datetime.date(2026, 6, 16),
                category="Alimentação",
                amount=Money("150"),
                description="Mercado",
            ),
            force=True,
        )
        # Category 2 under limits (50 spent / 200 limit)
        RegisterTransactionUseCase(tmp_repo).execute(
            Transaction(
                tx_id="tx-2",
                date=datetime.date(2026, 6, 16),
                category="Transporte",
                amount=Money("50"),
                description="Gasolina",
            )
        )
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)

        result = runner.invoke(app, ["status", "--month", "2026-06"])
        assert result.exit_code == 0
        assert "active" in result.output.lower()
        assert "spent: $200.00" in result.output.lower()
        assert "budget: $300.00" in result.output.lower()
        assert "remaining: $100.00" in result.output.lower()
        assert (
            "overrun category: 1" in result.output.lower()
            or "overrun: 1" in result.output.lower()
        )

    def test_status_fails_for_nonexistent_month(
        self,
        tmp_repo: FileLedgerRepository,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Querying status for a month with no budget must fail."""
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: tmp_repo)
        result = runner.invoke(app, ["status", "--month", "2026-07"])
        assert result.exit_code != 0
        assert "não encontrado" in result.output.lower()


# ---------------------------------------------------------------------------
# config.toml / storage
# ---------------------------------------------------------------------------


class TestConfigCommand:
    """Group: config.toml loading and fallback storage path."""

    def test_make_repo_respects_custom_data_dir(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When ~/.orcalogy/config.toml exists with storage.data_dir, we must use it."""
        config_dir = tmp_path / ".orcalogy"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        custom_data_dir = tmp_path / "custom_data"

        # Write config.toml using raw POSIX/Windows string representation
        escaped_path = str(custom_data_dir).replace("\\", "\\\\")
        config_file.write_text(
            f'[storage]\ndata_dir = "{escaped_path}"\n', encoding="utf-8"
        )

        # Mock the home path lookup in commands.py
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        from orcalogy.cli.commands import _make_repo

        repo = _make_repo()
        assert repo.data_dir == custom_data_dir

    def test_make_repo_falls_back_to_default_dir(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When config.toml is missing, _make_repo must default to ~/.orcalogy/data."""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        from orcalogy.cli.commands import _make_repo

        repo = _make_repo()
        expected = tmp_path / ".orcalogy" / "data"
        assert repo.data_dir == expected

    def test_init_creates_default_config_toml(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Running init for the first time must generate ~/.orcalogy/config.toml."""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        # Mock repository generation so it writes to our tmp_path
        from orcalogy.infra.file_repo import FileLedgerRepository

        data_dir = tmp_path / ".orcalogy" / "data"
        mock_repo = FileLedgerRepository(str(data_dir))
        monkeypatch.setattr("orcalogy.cli.commands._make_repo", lambda: mock_repo)

        config_file = tmp_path / ".orcalogy" / "config.toml"
        assert not config_file.exists()

        result = runner.invoke(app, ["init"], input="2026-06\nAlimentação\n500\n\n")
        assert result.exit_code == 0
        assert config_file.exists()
        assert "[storage]" in config_file.read_text(encoding="utf-8")

    def test_make_repo_handles_invalid_config_toml(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When config.toml is invalid, _make_repo must fallback to default path."""
        config_dir = tmp_path / ".orcalogy"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        # Write corrupted TOML content
        config_file.write_text("corrupted content [invalid storage\n", encoding="utf-8")

        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        from orcalogy.cli.commands import _make_repo

        repo = _make_repo()
        expected = tmp_path / ".orcalogy" / "data"
        assert repo.data_dir == expected
