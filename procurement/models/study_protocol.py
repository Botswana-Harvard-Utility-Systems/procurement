from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin


class ProtocolManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class StudyProtocol(SiteModelMixin, BaseUuidModel):

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=150, unique=True)

    objects = ProtocolManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'procurement'
