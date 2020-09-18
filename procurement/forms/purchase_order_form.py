from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
