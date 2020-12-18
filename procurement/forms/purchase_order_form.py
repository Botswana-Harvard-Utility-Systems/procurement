from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PurchaseOrder


class PurchaseOrderForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
        self.fields['order_number'].required = False

    order_number = forms.CharField(
        label='Purchase order number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
