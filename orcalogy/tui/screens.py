# ruff: noqa: E501, RUF001
"""Textual TUI screens for OrcaLogy.

Each class in this module represents a full-screen view or a modal dialog.
Now localized to Portuguese (PT-BR) with a friendly Main Menu and forms
accessible for laymen.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Any, ClassVar, cast

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Input, Label

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

if TYPE_CHECKING:
    from orcalogy.tui.app import OrcaLogyApp

_MAX_RECENT_TRANSACTIONS = 10


class MainMenuScreen(Screen[None]):
    """Main Menu Screen - welcoming laymen with a simple dashboard hub."""

    def compose(self) -> ComposeResult:
        month = datetime.date.today().strftime("%Y-%m")
        with Vertical(id="menu-container"):
            yield Label("🐳 OrcaLogy — Painel Financeiro Local", id="menu-title")
            yield Label(f"Mês Ativo de Referência: {month}", id="menu-subtitle")
            yield Label("\nSelecione uma opção abaixo:", id="menu-instructions")

            yield Button(
                "📊 Visualizar Painel do Mês (Dashboard)",
                id="btn-goto-dashboard",
                variant="primary",
            )
            yield Button(
                "➕ Registrar Nova Despesa (Transação)",
                id="btn-new-tx",
                variant="default",
            )
            yield Button(
                "⚙️ Criar / Configurar Orçamento Mensal",
                id="btn-init-budget",
                variant="default",
            )
            yield Button(
                "🔒 Fechar Ciclo Mensal (Bloquear Mês)",
                id="btn-close-cycle",
                variant="default",
            )
            yield Button("🚪 Sair do Aplicativo", id="btn-quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-goto-dashboard":
            self.app.push_screen(DashboardScreen())
        elif button_id == "btn-new-tx":
            self.app.push_screen(TransactionEntryDialog())
        elif button_id == "btn-init-budget":
            self.app.push_screen(BudgetInitDialog())
        elif button_id == "btn-close-cycle":
            self.app.push_screen(CloseCycleDialog())
        elif button_id == "btn-quit":
            self.app.exit()


class BudgetInitDialog(ModalScreen[None]):
    """Modal form for configuring a budget and categories in Portuguese."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancelar"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.categories: dict[str, Money] = {}

    def compose(self) -> ComposeResult:
        default_month = datetime.date.today().strftime("%Y-%m")
        with Vertical(id="dialog"):
            yield Label("Configurar Novo Orçamento", id="dialog-title")
            yield Input(
                value=default_month,
                placeholder="Mês (formato AAAA-MM, ex: 2026-06)",
                id="input-month",
            )

            yield Label("--- Adicionar Categoria ---", id="section-title")
            yield Input(
                placeholder="Nome da Categoria (ex: Alimentação)", id="input-cat-name"
            )
            yield Input(
                placeholder="Limite da Categoria (ex: 500.00)", id="input-cat-limit"
            )
            yield Button("Adicionar Categoria", id="btn-add-cat")

            yield Label("Categorias Adicionadas: Nenhuma", id="added-cats-label")
            yield Label("", id="dialog-error")

            with Horizontal(id="dialog-buttons"):
                yield Button("Salvar Orçamento", id="btn-save", variant="primary")
                yield Button("Cancelar", id="btn-cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-cancel":
            self.dismiss(None)
        elif button_id == "btn-add-cat":
            self._add_category()
        elif button_id == "btn-save":
            self._save_budget()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _add_category(self) -> None:
        name_input = self.query_one("#input-cat-name", Input)
        limit_input = self.query_one("#input-cat-limit", Input)
        error_label = self.query_one("#dialog-error", Label)

        name = name_input.value.strip()
        limit_str = limit_input.value.strip()

        if not name or not limit_str:
            error_label.update("Informe o nome e o limite da categoria.")
            return

        try:
            self.categories[name] = Money(limit_str)
            name_input.value = ""
            limit_input.value = ""
            error_label.update("")

            cats_text = ", ".join(f"{k} (R$ {v})" for k, v in self.categories.items())
            self.query_one("#added-cats-label", Label).update(
                f"Categorias Adicionadas: {cats_text}"
            )
        except (ValueError, TypeError) as exc:
            error_label.update(f"Valor limite inválido: {exc}")

    def _save_budget(self) -> None:
        month = self.query_one("#input-month", Input).value.strip()
        error_label = self.query_one("#dialog-error", Label)

        if not month:
            error_label.update("Informe o mês do orçamento.")
            return

        if not self.categories:
            error_label.update("Adicione pelo menos uma categoria.")
            return

        orca_app = cast("OrcaLogyApp", self.app)
        try:
            InitializeBudgetUseCase(orca_app.repository).execute(month, self.categories)
            self.dismiss(None)
        except ValueError as exc:
            error_label.update(str(exc))


class CloseCycleDialog(ModalScreen[None]):
    """Modal screen for locking/closing a budget period."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancelar"),
    ]

    def compose(self) -> ComposeResult:
        default_month = datetime.date.today().strftime("%Y-%m")
        with Vertical(id="dialog"):
            yield Label("Fechar Ciclo Mensal", id="dialog-title")
            yield Label(
                "Ao fechar o ciclo, novas transações serão bloqueadas permanentemente.",
                id="dialog-desc",
            )
            yield Input(
                value=default_month,
                placeholder="Mês (AAAA-MM, ex: 2026-06)",
                id="input-month",
            )
            yield Label("", id="dialog-error")

            with Horizontal(id="dialog-buttons"):
                yield Button("Confirmar Fechamento", id="btn-close", variant="primary")
                yield Button("Cancelar", id="btn-cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-cancel":
            self.dismiss(None)
        elif button_id == "btn-close":
            self._close_cycle()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _close_cycle(self) -> None:
        month = self.query_one("#input-month", Input).value.strip()
        error_label = self.query_one("#dialog-error", Label)

        if not month:
            error_label.update("Informe o mês.")
            return

        orca_app = cast("OrcaLogyApp", self.app)
        try:
            CloseBudgetCycleUseCase(orca_app.repository).execute(month)
            self.dismiss(None)
        except (BudgetNotFoundError, BudgetClosedError) as exc:
            error_label.update(str(exc))


class TransactionEntryDialog(ModalScreen[None]):
    """Modal form for entering a new transaction in Portuguese."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancelar"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._pending_tx: Transaction | None = None

    def compose(self) -> ComposeResult:
        from textual.suggester import SuggestFromList

        today = datetime.date.today().isoformat()
        orca_app = cast("OrcaLogyApp", self.app)
        month = datetime.date.today().strftime("%Y-%m")
        categories: list[str] = []

        try:
            budget = orca_app.repository.get_budget(month)
            if budget:
                categories = list(budget.categories.keys())
        except Exception:
            pass

        category_suggester = SuggestFromList(categories) if categories else None

        with Vertical(id="dialog"):
            yield Label("Registrar Nova Despesa", id="dialog-title")
            yield Input(
                placeholder="Categoria (ex: Alimentação)",
                id="input-category",
                suggester=category_suggester,
            )
            yield Input(placeholder="Valor (ex: 50.00)", id="input-amount")
            yield Input(
                placeholder="Descrição (ex: Almoço de negócios)", id="input-description"
            )
            yield Input(
                value=today,
                placeholder="Data (AAAA-MM-DD)",
                id="input-date",
            )
            yield Label("", id="dialog-error")
            with Horizontal(id="dialog-buttons"):
                yield Button("Registrar", id="btn-submit", variant="primary")
                yield Button("Cancelar", id="btn-cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-cancel":
            self.dismiss(None)
        elif button_id == "btn-submit":
            self._attempt_submit()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _attempt_submit(self) -> None:
        error_label = self.query_one("#dialog-error", Label)

        if self._pending_tx is not None:
            self._persist(self._pending_tx, force=True, error_label=error_label)
            return

        category = self.query_one("#input-category", Input).value.strip()
        amount_str = self.query_one("#input-amount", Input).value.strip()
        description = self.query_one("#input-description", Input).value.strip()
        date_str = self.query_one("#input-date", Input).value.strip()

        if not category or not amount_str:
            error_label.update("Categoria e Valor são obrigatórios.")
            return

        if date_str:
            try:
                tx_date = datetime.date.fromisoformat(date_str)
            except ValueError:
                error_label.update("Data inválida. Use AAAA-MM-DD.")
                return
        else:
            tx_date = datetime.date.today()

        try:
            tx = Transaction(
                tx_id=uuid.uuid4().hex[:8],
                date=tx_date,
                category=category,
                amount=Money(amount_str),
                description=description,
            )
        except (ValueError, TypeError) as exc:
            error_label.update(f"Entrada inválida: {exc}")
            return

        self._persist(tx, force=False, error_label=error_label)

    def _persist(self, tx: Transaction, force: bool, error_label: Label) -> None:
        orca_app = cast("OrcaLogyApp", self.app)

        try:
            RegisterTransactionUseCase(orca_app.repository).execute(tx, force=force)
        except BudgetOverrunError as exc:
            self._pending_tx = tx
            error_label.update(
                f"⚠️ Limite Excedido: {exc} — Clique em Registrar novamente para forçar."
            )
            return
        except (BudgetNotFoundError, BudgetClosedError) as exc:
            # Tradução de erros comuns de domínio
            msg = str(exc)
            if "not found" in msg.lower():
                msg = f"Orçamento para {tx.date.strftime('%Y-%m')} não foi encontrado. Crie um primeiro."
            elif "closed" in msg.lower():
                msg = "Este mês de orçamento já foi fechado e está bloqueado."
            error_label.update(msg)
            return

        self.dismiss(None)


class DashboardScreen(Screen[None]):
    """Dashboard Screen in Portuguese."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("r", "refresh_dashboard", "Atualizar"),
        Binding("n", "new_transaction", "Nova Despesa"),
        Binding("escape", "back_to_menu", "Menu Principal"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Desvios de Categoria", id="category-label")
        yield DataTable(id="category-table")
        yield Label(
            f"Transações Recentes (últimas {_MAX_RECENT_TRANSACTIONS})", id="tx-label"
        )
        yield DataTable(id="tx-table")

    def on_mount(self) -> None:
        self._populate()

    def action_refresh_dashboard(self) -> None:
        self._populate()

    def action_new_transaction(self) -> None:
        def _on_dismiss(_: None) -> None:
            self._populate()

        self.app.push_screen(TransactionEntryDialog(), _on_dismiss)

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()

    def _populate(self) -> None:
        orca_app = cast("OrcaLogyApp", self.app)
        month = datetime.date.today().strftime("%Y-%m")

        category_table: DataTable[Any] = self.query_one("#category-table", DataTable)
        tx_table: DataTable[Any] = self.query_one("#tx-table", DataTable)

        category_table.clear(columns=True)
        tx_table.clear(columns=True)

        try:
            ranking = GetCategoryDeviationRankingUseCase(orca_app.repository).execute(
                month
            )
        except BudgetNotFoundError:
            category_table.add_columns("Status")
            category_table.add_row(
                f"Nenhum orçamento encontrado para {month}. Volte e escolha 'Criar / Configurar Orçamento'."
            )
            tx_table.add_columns("Status")
            tx_table.add_row("Sem dados disponíveis.")
            return

        # Populate category deviation table - Color-coded
        category_table.add_columns(
            "Categoria", "Limite (R$)", "Gasto (R$)", "Desvio (%)"
        )
        for item in ranking:
            deviation_str = f"{item.deviation:+.2f}%"
            if item.deviation > 20:
                deviation_cell = Text(deviation_str, style="red")
            elif item.deviation > 0:
                deviation_cell = Text(deviation_str, style="yellow")
            else:
                deviation_cell = Text(deviation_str, style="green")

            category_table.add_row(
                item.category_name,
                str(item.limit.amount),
                str(item.spending.amount),
                deviation_cell,
            )

        # Populate recent transactions
        budget = orca_app.repository.get_budget(month)
        if budget and budget.transactions:
            tx_table.add_columns("Data", "Categoria", "Valor (R$)", "Descrição")
            recent = sorted(budget.transactions, key=lambda t: t.date, reverse=True)[
                :_MAX_RECENT_TRANSACTIONS
            ]
            for tx in recent:
                tx_table.add_row(
                    str(tx.date),
                    tx.category,
                    str(tx.amount.amount),
                    tx.description,
                )
        else:
            tx_table.add_columns("Status")
            tx_table.add_row("Nenhuma transação registrada ainda.")
