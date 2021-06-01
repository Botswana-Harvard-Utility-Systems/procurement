from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PurchaseInvoice


class PurchaseInvoiceForm(SiteModelFormMixin, forms.ModelForm):

    order_number = forms.CharField(
        label='Order number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = PurchaseInvoice
        fields = '__all__'
