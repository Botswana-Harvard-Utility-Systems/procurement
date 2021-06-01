from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .model_mixins import BaseLocatorDetailsMixin


class Customer(BaseLocatorDetailsMixin, SiteModelMixin, BaseUuidModel):

    account_number = models.CharField(
        max_length=50,
        unique=True)

    customer_ref = models.CharField(
        max_length=50,)

    class Meta:
        app_label = 'procurement'
