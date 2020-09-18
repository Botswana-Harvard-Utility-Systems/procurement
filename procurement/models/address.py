from django_crypto_fields.fields import EncryptedCharField
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import TelephoneNumber
from edc_base.sites.site_model_mixin import SiteModelMixin


class Address(SiteModelMixin, BaseUuidModel):

    telephone_contacts = EncryptedCharField(
        max_length=7,
        validators=[TelephoneNumber, ], )

    email = models.EmailField(max_length=150)

    fax = EncryptedCharField(
        max_length=7,
        validators=[TelephoneNumber], )

    physical_address = models.CharField(
        max_length=150)

    postal_address = models.CharField(
        max_length=150)

    def __str__(self):
        return f'{self.physical_address} {self.telephone_contacts} {self.email}'

    class Meta:
        app_label = 'procurement'
        verbose_name = 'Address'
        verbose_name_plural = 'Address'
