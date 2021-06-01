from django.db import models
from edc_base.model_mixins.base_uuid_model import BaseUuidModel

from .proxy_user import ProxyUser


class Signature(BaseUuidModel):

    owner = models.OneToOneField(ProxyUser, models.PROTECT)

    signature = models.ImageField(
        verbose_name='Upload copy of signature',
        upload_to='signatures/')

    def __str__(self):
        return f'{self.owner.first_name}\'s copy of signature'

    class Meta:
        app_label = 'procurement'
