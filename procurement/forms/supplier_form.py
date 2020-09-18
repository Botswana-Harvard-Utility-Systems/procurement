from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Supplier


class SupplierForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'
