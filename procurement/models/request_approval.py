from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin

from .proxy_user import ProxyUser
from ..choices import DOC_STATUS, REQUEST_REASON


class RequestApproval(SiteModelMixin, BaseUuidModel):

    document_id = models.CharField(
        verbose_name='Document Id',
        max_length=50, )

    request_by = models.ForeignKey(ProxyUser, models.PROTECT)

    def __str__(self):
        return f'{self.document_id}, {self.request_by}'

    class Meta:
        app_label = 'procurement'


class Request(BaseUuidModel):

    request_approval = models.ForeignKey(
        RequestApproval, on_delete=models.PROTECT)

    request_to = models.ForeignKey(ProxyUser, models.PROTECT)

    request_reason = models.CharField(
        max_length=100,
        choices=REQUEST_REASON)

    date_reviewed = models.DateField(blank=True, null=True)

    approval_sign = models.ImageField(
        verbose_name='Approval signature',
        upload_to='approval_signatures/',
        blank=True,
        null=True)

    status = models.CharField(
        max_length=8,
        choices=DOC_STATUS,
        default='new')

    comment = models.CharField(
        max_length=250,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta:
        app_label = 'procurement'
        unique_together = ('request_approval', 'request_to', 'status')
        ordering = ('date_reviewed', )
