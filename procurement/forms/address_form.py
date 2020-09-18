from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Address


class AddressForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'
