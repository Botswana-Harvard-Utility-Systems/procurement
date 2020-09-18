from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from . import Address


class CompanyManager(models.Manager):

    def get_by_natural_key(self, tax_registration):
        return self.get(
            tax_registration=tax_registration)

    class Meta:
        abstract = True


class Company(SiteModelMixin, BaseUuidModel):

    tax_registration = models.CharField(
        max_length=50,
        unique=True)

    name = models.CharField(max_length=150)

    address = models.ForeignKey(
        Address, on_delete=models.PROTECT)

    objects = CompanyManager()

    def __str__(self):
        return f'{self.tax_registration}'

    def natural_key(self):
        return (self.tax_registration,)

    class Meta:
        app_label = 'procurement'
        verbose_name = 'Company'
        verbose_name_plural = 'Company'
