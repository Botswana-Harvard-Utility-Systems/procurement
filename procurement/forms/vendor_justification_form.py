from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..form_validations import VendorJustificationFormValidator
from ..models import VendorJustification, CompetitiveBid


class VendorJustificationForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = VendorJustificationFormValidator

    justification_number = forms.CharField(
        label='Vendor justification number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        super().clean()

        if not self.data.get('competitivebid_set-0-vendor'):
            msg = {'__all__': 'Please complete the competitive bid table below.'}
            raise forms.ValidationError(msg)

    class Meta:
        model = VendorJustification
        fields = '__all__'


class CompetitveBidForm(forms.ModelForm):

    class Meta:
        model = CompetitiveBid
        fields = '__all__'
