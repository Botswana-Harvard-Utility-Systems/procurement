from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin


class ReportEmail(SiteModelMixin, BaseUuidModel):

    sender_email = models.EmailField()

    receipient_email = models.EmailField()

    subject = models.CharField(max_length=250)

    message = models.TextField()

    def __str__(self):
        return f'Report email sent to {self.email}'

    class Meta:
        app_label = 'procurement'
