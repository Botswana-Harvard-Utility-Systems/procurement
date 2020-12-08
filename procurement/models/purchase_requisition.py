from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base

from .model_mixins import PurchaseItemMixin
from .proxy_user import ProxyUser
from .study_protocol import StudyProtocol
from ..choices import ALLOCATION_TYPE
from ..identifiers import PurchaseRequisitionIdentifier


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('prf_number')
        return fields

    class Meta:
        abstract = True


class PurchaseRequisitionManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, prf_number):
        return self.get(
            prf_number=prf_number)

    class Meta:
        abstract = True


class PurchaseRequisition(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    identifier_cls = PurchaseRequisitionIdentifier

    prf_number = models.CharField(
        verbose_name='Purchase requisition number',
        max_length=50,
        unique=True,)

    req_date = models.DateField(
        verbose_name='Requisition date',
        default=get_utcnow)

    reason = models.CharField(
        verbose_name='Reason for request',
        max_length=100)

    allocation_type = models.CharField(
        choices=ALLOCATION_TYPE,
        max_length=5)

    request_by = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE)

    approval_by = models.CharField(
        verbose_name='Approved by',
        max_length=100,
        help_text='First and Last name',
        blank=True,
        null=True,)

    approved = models.BooleanField(default=False, editable=False)

    funds_confirmed = models.CharField(
        verbose_name='Availability of funds confirmed by',
        max_length=100,
        blank=True,
        null=True,
        help_text='First and Last name')

    objects = PurchaseRequisitionManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.prf_number} requested by: {self.request_by}'

    def natural_key(self):
        return (self.order_number,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.prf_number = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'procurement'


class Allocation(BaseUuidModel):

    purchase_req = models.ForeignKey(PurchaseRequisition, on_delete=models.PROTECT)

    bhp_allocation = models.ForeignKey(StudyProtocol, on_delete=models.PROTECT)

    percentage = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.bhp_allocation.name}, {self.percentage}%'

    class Meta:
        app_label = 'procurement'


class Quotation(BaseUuidModel):

    purchase_req = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE)

    quotes = models.FileField(upload_to='quotations/')

    def __str__(self):
        return f'{self.purchase_req.prf_number}'

    class Meta:
        app_label = 'procurement'


class PurchaseRequisitionItem(PurchaseItemMixin, BaseUuidModel):

    purchase_req = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE)

    class Meta:
        app_label = 'procurement'
