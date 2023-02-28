from django.conf import settings
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from src.apps.deals.models import Deal


def get_top_customers():
    return (
        Deal.objects.values("customer")
        .annotate(spent_money=Coalesce(Sum("total"), 0, output_field=DecimalField()))
        .order_by("-spent_money")[: settings.CUSTOMER_LIST_QUANTITY]
    )


def get_gems_for_customers(customers: list[str]) -> dict:
    deals = (
        Deal.objects.filter(customer__in=customers)
        .values("customer", "item")
        .distinct()
    )

    gems = {}
    for deal in deals:
        if deal["customer"] not in gems:
            gems[deal["customer"]] = set()

        gems[deal["customer"]].add(deal["item"])
    return gems


def get_top_customers_with_gems():
    top_customers = get_top_customers()
    top_customers_names = [customer["customer"] for customer in top_customers]
    gems = get_gems_for_customers(customers=top_customers_names)

    result = []
    for customer in top_customers:
        result_gems = list()
        for other_customer in top_customers_names:
            if other_customer != customer["customer"] and other_customer in gems:
                result_gems += list(gems[customer["customer"]] & gems[other_customer])

        spent_money = customer["spent_money"]
        result.append(
            {
                "customer": customer["customer"],
                "gems": result_gems,
                "spent_money": spent_money,
            }
        )

    return result
