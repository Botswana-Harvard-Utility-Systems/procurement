from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import StudyProtocol


class StudyProtocolForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = StudyProtocol
        fields = '__all__'
