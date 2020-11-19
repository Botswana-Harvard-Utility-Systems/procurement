from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base

from .list_models import CostAnalysis
from .supplier import Supplier
from ..choices import NOT_LOWEST_BID
from ..identifiers import VendorJustificationIdentifier


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('vj_number')
        return fields

    class Meta:
        abstract = True


class VendorJustificationManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, justification_number):
        return self.get(
            justification_number=justification_number)

    class Meta:
        abstract = True


class VendorJustification(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    identifier_cls = VendorJustificationIdentifier

    justification_number = models.CharField(
        verbose_name='Vendor justification number',
        max_length=50,
        unique=True)

    prf_number = models.CharField(
        verbose_name='Purchase requisition number',
        max_length=50)

    date = models.DateField(
        default=get_utcnow)

    selected_vendor = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    not_lowest_bid = models.CharField(
        verbose_name='If the lowest bidder was not chosen, select ONE',
        choices=NOT_LOWEST_BID,
        max_length=100,
        blank=True,
        null=True)

    selected_source_explain = models.TextField(
        max_length=500,
        verbose_name=('Identify other sources considered and on what basis they '
                      'were rejected'),
        blank=True,
        null=True)

    sole_source_explain = models.TextField(
        max_length=500,
        blank=True,
        null=True)

    cost_analysis = models.ManyToManyField(
        CostAnalysis,
        blank=True,
        help_text=('Select one or more of these statements to indicate that the '
                   'bid price was fair and reasonable'))

    voucher_no = models.CharField(
        verbose_name='Voucher no.',
        max_length=50,
        blank=True,
        null=True)

    cost_analysis_other = OtherCharField()

    objects = VendorJustificationManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.justification_number}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.justification_number = self.identifier_cls().identifier
        super().save(*args, **kwargs)


class CompetitiveBid(BaseUuidModel):

    vendor_justification = models.ForeignKey(VendorJustification, on_delete=models.CASCADE)

    vendor = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    bid_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.purchase_req.prf_number}'

    class Meta:
        app_label = 'procurement'
