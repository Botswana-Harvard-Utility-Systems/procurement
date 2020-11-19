from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import VendorJustification, CompetitiveBid


class VendorJustificationForm(SiteModelFormMixin, forms.ModelForm):

    justification_number = forms.CharField(
        label='Vendor justification number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = VendorJustification
        fields = '__all__'


class CompetitveBidForm(forms.ModelForm):

    class Meta:
        model = CompetitiveBid
        fields = '__all__'
