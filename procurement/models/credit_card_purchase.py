from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base

from .proxy_user import ProxyUser
from .study_protocol import StudyProtocol
from ..identifiers import CreditCardPurchaseIdentifier
from edc_constants.choices import YES_NO


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('ccp_number')
        return fields

    class Meta:
        abstract = True


class CreditCardPurchaseManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, ccp_number):
        return self.get(
            ccp_number=ccp_number)

    class Meta:
        abstract = True


class CreditCardPurchase(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    identifier_cls = CreditCardPurchaseIdentifier

    ccp_number = models.CharField(
        verbose_name='Purchase requisition number',
        max_length=50,
        unique=True,)

    req_date = models.DateField(
        verbose_name='Requisition date',
        default=get_utcnow)

    grant_chargeable = models.ForeignKey(StudyProtocol, on_delete=models.PROTECT)

    description = models.TextField(
        verbose_name='Description of Goods/Services',
        max_length=200)

    accomodation = models.CharField(
        verbose_name='Is the card used to reserve accomodation?',
        choices=YES_NO,
        max_length=3)

    card_paid_accomo = models.CharField(
        verbose_name='Will the accomodation be paid from the Credit Card?',
        choices=YES_NO,
        max_length=3)

    currency = models.CharField(
        verbose_name='Currency used',
        max_length=10)

    total_amount = models.DecimalField(decimal_places=2, max_digits=10)

    alt_provider = models.CharField(
        verbose_name='Is there an alternative service provider?',
        choices=YES_NO,
        max_length=3)

    selected_vendor = models.CharField(
        verbose_name='If yes, state reason(s) for the selected vendor',
        max_length=250,
        blank=True,
        null=True)

    checkout_copy = models.FileField(upload_to='checkout_copies/')

    card_holder = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE)

    request_by = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE,
        related_name='cc_request_by',)

    approval_by = models.ForeignKey(
        ProxyUser, on_delete=models.CASCADE,
        related_name='cc_approval_by',
        blank=True,
        null=True)

    approved = models.BooleanField(default=False, editable=False)

    status = models.CharField(
        max_length=10,
        default='new')

    objects = CreditCardPurchaseManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.ccp_number} requested by: {self.request_by}'

    def natural_key(self):
        return (self.ccp_number,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.ccp_number = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'procurement'
        verbose_name = 'Credit Card Authorization'
