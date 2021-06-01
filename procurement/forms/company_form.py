from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Company


class CompanyForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
