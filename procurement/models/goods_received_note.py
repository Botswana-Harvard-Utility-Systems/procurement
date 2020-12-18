from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from .supplier import Supplier


class GoodsReceivedNote(SiteModelMixin, BaseUuidModel):

    grn_number = models.CharField(
        verbose_name='Goods received number',
        max_length=50,
        unique=True,)

    order_number = models.CharField(
        verbose_name='Purchase order number',
        max_length=50,)

    vendor = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    date_received = models.DateField(default=get_utcnow)

    delivery_note_attached = models.CharField(
        choices=YES_NO,
        max_length=3)

    delivery_note = models.FileField(
        upload_to='delivery_notes/', blank=True, null=True)

    received_by = models.CharField(max_length=50)

    delivered_by = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.grn_number}, for order {self.order_number}'

    def save(self, *args, **kwargs):
        self.received_by = f'{self.request.user.first_name} {self.request.user.last_name}'
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'procurement'


class DeliveredItem(BaseUuidModel):

    grn = models.ForeignKey(GoodsReceivedNote, on_delete=models.CASCADE)

    description = models.CharField(max_length=100)

    order_quantity = models.PositiveIntegerField()

    delivered_quantity = models.PositiveIntegerField()

    class Meta:
        app_label = 'procurement'
