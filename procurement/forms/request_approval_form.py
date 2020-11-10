from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import RequestApproval


class RequestApprovalForm(SiteModelFormMixin, forms.ModelForm):

    document_id = forms.CharField(
        label='Document Id',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    request_by = forms.CharField(
        label='Requested by',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    status = forms.CharField(
        label='Status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = RequestApproval
        fields = '__all__'
