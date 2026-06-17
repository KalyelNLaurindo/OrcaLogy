"""Typer CLI application controller for OrcaLogy.

Wires up all CLI subcommands (init, add, report) and the root entry point.
Each command bootstraps its own repository so the domain layer stays clean.
"""

import datetime
import uuid
from pathlib import Path

import typer

from orcalogy.app.services import (
    GetCategoryDeviationRankingUseCase,
    InitializeBudgetUseCase,
    RegisterTransactionUseCase,
)
from orcalogy.domain.errors import BudgetNotFoundError, BudgetOverrunError
from orcalogy.domain.models import Money, Transaction
from orcalogy.infra.file_repo import FileLedgerRepository

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
    """Create a FileLedgerRepository pointing to the default user data directory."""
    data_dir = Path.home() / ".orcalogy" / "data"
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
    if version:
        typer.echo(f"orca version {VERSION}")
        raise typer.Exit()


@app.command("init")
def init() -> None:
    """Create a new monthly budget and define spending limits per category."""
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
