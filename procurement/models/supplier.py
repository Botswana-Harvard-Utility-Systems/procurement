from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_constants.choices import YES_NO

from .model_mixins import BaseLocatorDetailsMixin
from ..choices import SUPPLIER_GROUP, CURRENCY


class SupplierManager(models.Manager):

    def get_by_natural_key(self, supplier_identifier):
        return self.get(
            supplier_identifier=supplier_identifier)

    class Meta:
        abstract = True


class Supplier(BaseLocatorDetailsMixin, SiteModelMixin, BaseUuidModel):

    supplier_identifier = models.CharField(
        max_length=50,
        unique=True)

    supplier = models.CharField(max_length=150)

    supplier_locality = models.CharField(
        verbose_name='Is this supplier local or international?',
        choices=YES_NO,
        max_length=3)

    supplier_group = models.CharField(
        max_length=15,
        choices=SUPPLIER_GROUP,
        help_text='Select appropriate supplier group.')

    currency = models.CharField(
        verbose_name=('If foreign account, please indicate in which currency,'
                      ' the supplier should be maintained.'),
        choices=CURRENCY,
        max_length=3,
        blank=True,
        null=True)

    objects = SupplierManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}, Group: {self.supplier_group}'

    def natural_key(self):
        return (self.supplier_identifier,)

    class Meta:
        app_label = 'procurement'
