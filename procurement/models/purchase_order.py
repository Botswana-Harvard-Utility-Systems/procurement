from django.contrib.auth.models import User
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow

from .study_protocol import StudyProtocol
from .model_mixins import PurchaseItemMixin
from .company import Company
from .supplier import Supplier
from ..identifiers import PurchaseOrderIdentifier


class PurchaseOrderManager(models.Manager):

    def get_by_natural_key(self, order_number):
        return self.get(
            order_number=order_number)

    class Meta:
        abstract = True


class PurchaseOrder(SiteModelMixin, BaseUuidModel):

    identifier_cls = PurchaseOrderIdentifier

    order_number = models.CharField(
        verbose_name='Purchase order number',
        max_length=50,
        unique=True,)

    order_date = models.DateField(
        verbose_name='Purchase order date',
        default=get_utcnow)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    vendor = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    agent = models.ForeignKey(User, on_delete=models.CASCADE)

    bhp_allocation = models.ForeignKey(StudyProtocol, on_delete=models.PROTECT)

    objects = PurchaseOrderManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.order_number} prepared by: {self.agent}'

    def natural_key(self):
        return (self.order_number,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.order_number = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'procurement'


class PurchaseOrderItem(PurchaseItemMixin, BaseUuidModel):

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)

    class Meta:
        app_label = 'procurement'
