from django.contrib.auth.models import User
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin


class RequestApproval(SiteModelMixin, BaseUuidModel):

    rfa_number = models.CharField(
        verbose_name='Request for approval id',
        max_length=50,
        unique=True, )

    prf_number = models.CharField(
        verbose_name='Purchase requisition number',
        max_length=50, )

    request_by = models.CharField(
        verbose_name='Requested by',
        max_length=100,
        help_text='First and Last name')

    request_to = models.ForeignKey(User, models.PROTECT)

    approval_sign = models.ImageField(upload_to='approval_signatures/')

    class Meta:
        app_label = 'procurement'
