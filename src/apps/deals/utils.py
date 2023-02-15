from typing import Any

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, FloatField, QuerySet, Case, When

from src.apps.deals.models import Deal


def _get_top_by_spent_money(queryset) -> QuerySet[dict[str, Any]]:
    return (
        queryset.values("customer")
        .order_by("customer")
        .annotate(spent_money=Sum("total", output_field=FloatField()))
        .order_by("-spent_money")[: settings.CUSTOMER_LIST_QUANTITY]
    )


def _add_spent_money_and_gems(data: QuerySet[dict[str, Any]]) -> list[Deal]:
    result = []
    for row in data:
        deal = Deal.objects.filter(customer=row["customer"]).first()
        deal.spent_money = row["spent_money"]
        other_customers_gems = Deal.objects.filter(
            customer__in=[
                tmp_deal["customer"]
                for tmp_deal in data
                if tmp_deal["customer"] != deal.customer
            ]
        ).aggregate(gems=ArrayAgg("item", distinct=True))["gems"]
        deal.gems = [
            gem
            for gem in Deal.objects.filter(customer=deal.customer).aggregate(
                gems=ArrayAgg(
                    Case(
                        When(item__in=other_customers_gems, then="item"),
                        default=None,
                    ),
                    distinct=True,
                )
            )["gems"]
            if gem
        ]
        result.append(deal)

    return result


def deals_queryset(queryset):
    data = _get_top_by_spent_money(queryset)
    return _add_spent_money_and_gems(data)
