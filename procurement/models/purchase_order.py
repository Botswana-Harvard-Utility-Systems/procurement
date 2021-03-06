from django.conf import settings
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base

from .company import Company
from .proxy_user import ProxyUser
from ..identifiers import PurchaseOrderIdentifier


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('order_number')
        return fields

    class Meta:
        abstract = True


class PurchaseOrderManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, order_number):
        return self.get(
            order_number=order_number)

    class Meta:
        abstract = True


class PurchaseOrder(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    identifier_cls = PurchaseOrderIdentifier

    order_number = models.CharField(
        verbose_name='Purchase order number',
        max_length=50,
        unique=True,)

    prf_number = models.CharField(
        verbose_name='Purchase requisition number',
        max_length=50,)

    order_date = models.DateField(
        verbose_name='Purchase order date',
        default=get_utcnow)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    first_approver = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE,
        related_name='first_approver',
        blank=True,
        null=True)

    second_approver = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE,
        related_name='second_approver',
        blank=True,
        null=True)

    authorised = models.BooleanField(default=False, editable=False)

    file = models.FileField(
        upload_to='purchase_orders/', blank=True, null=True)

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
