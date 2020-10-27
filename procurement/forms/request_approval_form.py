from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import RequestApproval


class RequestApprovalForm(SiteModelFormMixin, forms.ModelForm):

    rfa_number = forms.CharField(
        label='Request approval number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    request_by = forms.CharField(
        label='Requested by',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = RequestApproval
        fields = '__all__'
