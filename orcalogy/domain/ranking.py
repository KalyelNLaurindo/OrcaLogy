from dataclasses import dataclass
from decimal import Decimal

from orcalogy.domain.models import Budget, Money


@dataclass(frozen=True)
class CategoryRankingItem:
    """DTO representing a category budget deviation item for reporting."""

    category_name: str
    limit: Money
    spending: Money
    deviation: Decimal


def calculate_ranking(budget: Budget) -> list[CategoryRankingItem]:
    """Calculate percentage deviation for each category and sort descending."""
    items = []
    for name, category in budget.categories.items():
        spending = budget.get_category_spending(name)
        limit_val = category.limit.amount
        spending_val = spending.amount

        if limit_val == Decimal("0.00"):
            if spending_val == Decimal("0.00"):
                deviation = Decimal("0.00")
            else:
                deviation = Decimal("100.00")
        else:
            # Formula: ((spending / limit) - 1) * 100
            ratio = spending_val / limit_val
            raw_deviation = (ratio - Decimal("1.00")) * Decimal("100.00")
            deviation = raw_deviation.quantize(
                Decimal("0.01"), rounding="ROUND_HALF_UP"
            )

        items.append(
            CategoryRankingItem(
                category_name=name,
                limit=category.limit,
                spending=spending,
                deviation=deviation,
            )
        )

    # Sort descending by deviation percentage
    items.sort(key=lambda x: x.deviation, reverse=True)
    return items
