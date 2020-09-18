from django.db import models


class PurchaseItemMixin(models.Model):

    description = models.CharField(max_length=200)

    item_code = models.CharField(max_length=200)

    quantity_ordered = models.PositiveIntegerField()

    unit_price = models.DecimalField(decimal_places=2, max_digits=10)

    discount = models.DecimalField(
        blank=True, null=True,
        decimal_places=2, max_digits=10,
        help_text='Percentage (%) discount')

    total_price_excl = models.DecimalField(decimal_places=2, max_digits=10)

    vat = models.DecimalField(decimal_places=2, max_digits=10)

    total_price_incl = models.DecimalField(decimal_places=2, max_digits=10)

    def save(self, *args, **kwargs):
        total = (self.quantity_ordered * self.unit_price - (self.discount/100))
        self.total_price_excl = total
        self.total_price_incl = self.total_price_excl + (
            self.total_price_excl * 0.12)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
