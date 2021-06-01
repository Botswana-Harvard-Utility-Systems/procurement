from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Invoice, InvoiceItem


class InvoiceForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemForm(forms.ModelForm):

    class Meta:
        model = InvoiceItem
        fields = '__all__'
