from django.db import models
from django.utils.translation import gettext_lazy as _


class Deal(models.Model):
    customer = models.CharField(_("Login of Customer"), max_length=120)
    item = models.CharField(_("Name of Good"), max_length=120)
    total = models.DecimalField(
        _("Total Price of Good"), max_digits=10, decimal_places=2
    )
    quantity = models.PositiveSmallIntegerField(_("Quantity of Goods"))
    date = models.DateTimeField(_("Date of Deal registration"))
