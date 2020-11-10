from django.contrib.auth.models import User
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin


class RequestApproval(SiteModelMixin, BaseUuidModel):

    document_id = models.CharField(
        verbose_name='Document Id',
        max_length=50, )

    request_by = models.CharField(
        verbose_name='Requested by',
        max_length=100,
        help_text='First and Last name')

    request_to = models.ForeignKey(User, models.PROTECT,)

    approval_sign = models.ImageField(
        verbose_name='Approval signature',
        upload_to='approval_signatures/',
        blank=True,
        null=True)

    status = models.CharField(max_length=8)

    class Meta:
        app_label = 'procurement'
