from django.contrib.auth.models import User
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow

from .company import Company
from .customer import Customer
from .model_mixins import PurchaseItemMixin


class InvoiceManager(models.Manager):

    def get_by_natural_key(self, invoice_number):
        return self.get(
            invoice_number=invoice_number)

    class Meta:
        abstract = True


class Invoice(SiteModelMixin, BaseUuidModel):

    invoice_number = models.CharField(
        verbose_name='Invoice number',
        max_length=50,
        unique=True)

    invoice_date = models.DateField(
        verbose_name='Purchase order date',
        default=get_utcnow)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE)

    order_number = models.CharField(
        verbose_name='Order number',
        max_length=50,)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    objects = InvoiceManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.invoice_number} prepared by: {self.agent}'

    def natural_key(self):
        return (self.invoice_number,)

    class Meta:
        app_label = 'procurement'


class InvoiceItem(PurchaseItemMixin, BaseUuidModel):

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)

    class Meta:
        app_label = 'procurement'
