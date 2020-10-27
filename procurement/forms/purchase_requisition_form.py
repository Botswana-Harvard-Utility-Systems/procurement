from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PurchaseRequisition, PurchaseRequisitionItem, Quotation


class PurchaseRequisitionForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurchaseRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['prf_number'].required = False

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    approval_by = forms.CharField(
        label='Approval by',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    funds_confirmed = forms.CharField(
        label='Availability of funds confirmed by',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = PurchaseRequisition
        fields = '__all__'


class PurchaseRequisitionItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseRequisitionItem
        fields = '__all__'


class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotation
        fields = '__all__'
