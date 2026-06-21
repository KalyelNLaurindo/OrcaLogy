"""Typer CLI application controller for OrcaLogy.

Wires up all CLI subcommands (init, add, report) and the root entry point.
Each command bootstraps its own repository so the domain layer stays clean.
"""

import datetime
import uuid
from pathlib import Path

import typer

from orcalogy.app.services import (
    CloseBudgetCycleUseCase,
    GetCategoryDeviationRankingUseCase,
    InitializeBudgetUseCase,
    RegisterTransactionUseCase,
)
from orcalogy.domain.errors import (
    BudgetClosedError,
    BudgetNotFoundError,
    BudgetOverrunError,
)
from orcalogy.domain.models import Money, Transaction
from orcalogy.infra.file_repo import FileLedgerRepository
from orcalogy.tui.app import OrcaLogyApp

VERSION = "0.1.0"

# ANSI colour constants — used directly to guarantee codes appear in output.
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"
_RESET = "\033[0m"

app = typer.Typer(
    name="orca",
    help="OrcaLogy — local-first budget management CLI.",
    no_args_is_help=True,
    invoke_without_command=True,
    add_completion=True,
)


def _make_repo() -> FileLedgerRepository:
    """Create a FileLedgerRepository pointing to the user data directory.

    Reads the configuration file if it exists, otherwise falls back to default.
    """
    home_dir = Path.home() / ".orcalogy"
    config_file = home_dir / "config.toml"
    data_dir = home_dir / "data"

    if config_file.exists():
        try:
            import tomllib
            with config_file.open("rb") as f:
                data = tomllib.load(f)
            custom_dir = data.get("storage", {}).get("data_dir", None)
            if custom_dir:
                data_dir = Path(custom_dir)
        except Exception:
            pass

    data_dir.mkdir(parents=True, exist_ok=True)
    return FileLedgerRepository(str(data_dir))


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-V",
        is_eager=True,
        help="Show the installed OrcaLogy version and exit.",
    ),
) -> None:
    """OrcaLogy budget CLI — run a subcommand or use --help."""
    from orcalogy.main import setup_logging
    setup_logging()

    if version:
        typer.echo(f"orca version {VERSION}")
        raise typer.Exit()


@app.command("init")
def init() -> None:
    """Create a new monthly budget and define spending limits per category."""
    # Ensure config.toml exists on first run
    home_dir = Path.home() / ".orcalogy"
    home_dir.mkdir(parents=True, exist_ok=True)
    config_file = home_dir / "config.toml"
    if not config_file.exists():
        escaped_data_dir = str(home_dir / "data").replace("\\", "\\\\")
        default_config = f'[storage]\ndata_dir = "{escaped_data_dir}"\n'
        config_file.write_text(default_config, encoding="utf-8")

    month = typer.prompt("Mês (YYYY-MM)")

    category_limits: dict[str, Money] = {}
    typer.echo("Categorias (enter vazio para terminar):")
    while True:
        name = typer.prompt("  Nome da categoria", default="")
        if not name:
            break
        limit_str = typer.prompt("  Limite (CAD)")
        try:
            category_limits[name] = Money(limit_str)
        except (ValueError, TypeError) as exc:
            typer.echo(f"  Valor inválido: {exc}")

    if not category_limits:
        typer.echo("Erro: informe ao menos uma categoria.")
        raise typer.Exit(1)

    repo = _make_repo()
    try:
        InitializeBudgetUseCase(repo).execute(month, category_limits)
        n = len(category_limits)
        typer.echo(f"✅ Orçamento {month} criado com {n} categoria(s).")
    except ValueError as exc:
        typer.echo(f"Erro: {exc}")
        raise typer.Exit(1) from exc


@app.command("add")
def add_transaction(
    category: str = typer.Option(..., "--category", "-c", help="Category name"),
    amount: str = typer.Option(..., "--amount", "-a", help="Amount (e.g. 150.00)"),
    description: str = typer.Option(..., "--description", "-d", help="Description"),
    date: str = typer.Option(..., "--date", help="Date in YYYY-MM-DD format"),
) -> None:
    """Register a spending transaction in the monthly budget."""
    try:
        parsed_date = datetime.date.fromisoformat(date)
    except ValueError:
        typer.echo(f"Erro: data inválida '{date}'. Use o formato YYYY-MM-DD.")
        raise typer.Exit(1) from None

    try:
        parsed_amount = Money(amount)
    except (ValueError, TypeError) as exc:
        typer.echo(f"Erro: valor inválido '{amount}'. {exc}")
        raise typer.Exit(1) from exc

    transaction = Transaction(
        tx_id=str(uuid.uuid4()),
        date=parsed_date,
        category=category,
        amount=parsed_amount,
        description=description,
    )

    repo = _make_repo()
    use_case = RegisterTransactionUseCase(repo)

    try:
        use_case.execute(transaction)
        typer.echo("✅ Transação registrada.")
    except BudgetOverrunError as exc:
        typer.echo(f"⚠️  ALERTA: {exc}")
        if typer.confirm("Forçar o registro mesmo assim?", default=False):
            use_case.execute(transaction, force=True)
            typer.echo("✅ Transação registrada com força.")
        else:
            typer.echo("Operação cancelada.")
    except BudgetClosedError as exc:
        typer.echo(f"Erro: o ciclo de orçamento está fechado. {exc}")
        raise typer.Exit(1) from exc



@app.command("tui")
def tui(
    data_dir: str = typer.Option(
        str(Path.home() / ".orcalogy" / "data"),
        "--data-dir",
        help="Path to the data directory (defaults to ~/.orcalogy/data).",
    ),
) -> None:
    """Launch the interactive TUI dashboard."""
    dir_path = Path(data_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    repo = FileLedgerRepository(str(dir_path))
    OrcaLogyApp(repository=repo).run()


@app.command("report")
def report(
    month: str = typer.Option(..., "--month", "-m", help="Budget period (YYYY-MM)"),
) -> None:
    """Show a color-coded spending deviation report for a budget month."""
    repo = _make_repo()
    try:
        ranking = GetCategoryDeviationRankingUseCase(repo).execute(month)
    except BudgetNotFoundError:
        typer.echo(f"Erro: orçamento para '{month}' não encontrado.")
        raise typer.Exit(1) from None

    typer.echo(f"\nRelatório — Orçamento {month}")
    typer.echo("─" * 58)
    typer.echo(f"{'Categoria':<22} {'Limite':>8} {'Gasto':>8} {'Desvio':>8}")
    typer.echo("─" * 58)

    for item in ranking:
        deviation_str = f"{item.deviation:+.2f}%"
        row = (
            f"{item.category_name:<22}"
            f" {item.limit.amount!s:>8}"
            f" {item.spending.amount!s:>8}"
            f" {deviation_str:>8}"
        )
        # Colour the row based on how far over or under the category limit is.
        if item.deviation <= 0:
            typer.echo(f"{_GREEN}{row}{_RESET}")
        elif item.deviation <= 20:
            typer.echo(f"{_YELLOW}{row}{_RESET}")
        else:
            typer.echo(f"{_RED}{row}{_RESET}")

    typer.echo("─" * 58)


@app.command("close")
def close(
    month: str = typer.Option(
        ..., "--month", "-m", help="Budget month to close (YYYY-MM)"
    ),
) -> None:
    """Close the budget cycle for a specific month, locking it from further changes."""
    repo = _make_repo()
    try:
        CloseBudgetCycleUseCase(repo).execute(month)
        typer.echo(f"✅ Ciclo de orçamento {month} fechado com sucesso.")
    except BudgetNotFoundError:
        typer.echo(f"Erro: orçamento para '{month}' não encontrado.")
        raise typer.Exit(1) from None
    except BudgetClosedError:
        typer.echo(f"Erro: o ciclo de orçamento para '{month}' já está fechado.")
        raise typer.Exit(1) from None


@app.command("status")
def status(
    month: str = typer.Option(
        ..., "--month", "-m", help="Budget month to query (YYYY-MM)"
    ),
) -> None:
    """Show a lightweight snapshot overview of the budget period."""
    repo = _make_repo()
    budget = repo.get_budget(month)
    if budget is None:
        typer.echo(f"Erro: orçamento para '{month}' não encontrado.")
        raise typer.Exit(1)

    # Calculate consolidations
    total_budget = Money("0.00")
    for category in budget.categories.values():
        total_budget += category.limit

    total_spent = budget.get_total_spending()
    remaining = total_budget - total_spent

    overrun_count = 0
    for cat_name, category in budget.categories.items():
        cat_spending = budget.get_category_spending(cat_name)
        if cat_spending > category.limit:
            overrun_count += 1

    typer.echo(f"Status: {budget.status}")
    typer.echo(f"Budget: {total_budget}")
    typer.echo(f"Spent: {total_spent}")
    typer.echo(f"Remaining: {remaining}")
    typer.echo(f"Overrun: {overrun_count}")


