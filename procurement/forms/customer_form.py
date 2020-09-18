from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Customer


class CustomerForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
