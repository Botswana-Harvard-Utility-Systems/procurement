from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow

from .supplier import Supplier
from .company import Company


class PurchaseInvoiceManager(models.Manager):

    def get_by_natural_key(self, invoice_number):
        return self.get(
            invoice_number=invoice_number)

    class Meta:
        abstract = True


class PurchaseInvoice(SiteModelMixin, BaseUuidModel):

    invoice_number = models.CharField(
        verbose_name='Invoice number',
        max_length=50,
        unique=True)

    invoice_date = models.DateField(default=get_utcnow)

    vendor = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    order_number = models.CharField(
        verbose_name='Order number',
        max_length=50,)

    paid = models.BooleanField(default=False)

    published = models.BooleanField(default=False)

    document = models.FileField(upload_to='invoices/')

    objects = PurchaseInvoiceManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'Purchase invoice from {self.vendor.name}'

    class Meta:
        app_label = 'procurement'
