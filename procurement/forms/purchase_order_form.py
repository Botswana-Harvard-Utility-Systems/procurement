from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
        self.fields['order_number'].required = False

    order_number = forms.CharField(
        label='Purchase order number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
