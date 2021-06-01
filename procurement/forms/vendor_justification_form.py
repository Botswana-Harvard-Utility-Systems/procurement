from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..form_validations import FormCalculationsMixin, VendorJustificationFormValidator
from ..models import VendorJustification, CompetitiveBid


class VendorJustificationForm(
        SiteModelFormMixin, FormValidatorMixin, FormCalculationsMixin, forms.ModelForm):

    form_validator_cls = VendorJustificationFormValidator

    justification_number = forms.CharField(
        label='Vendor justification number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    prf_number = forms.CharField(
        label='Purchase requisition number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = super().clean()

        if not self.data.get('competitivebid_set-0-vendor'):
            msg = {'__all__': 'Please complete the competitive bid table below.'}
            raise forms.ValidationError(msg)

        total_bids = self.data.get('competitivebid_set-TOTAL_FORMS')

        if int(total_bids) > 1 and cleaned_data.get('not_lowest_bid') == 'sole_source':
            msg = {'not_lowest_bid':
                   'Vendor is said to be sole source but more than 1 competitive '
                   'bids have been specified. Please correct this.'}
            raise forms.ValidationError(msg)

        prf_number = cleaned_data.get('prf_number')

        bid_match = self.check_bid_price_match_prf_total(prf_number, total_bids)

        if not bid_match[0]:
            msg = {'__all__':
                   f'Total price incl. of vat for purchase requisition is {bid_match[1]}'
                   ' atleast one of the vendors bid price should match this.'}
            raise forms.ValidationError(msg)

    def check_bid_price_match_prf_total(self, prf_number, total_bids):
        check = False
        total_costs = self.items_total_cost(prf_number)

        for num in range(int(total_bids)):
            bid_price = self.data.get(f'competitivebid_set-{num}-bid_price')

            if total_costs == float(bid_price):
                check = True
        return [check, total_costs]

    class Meta:
        model = VendorJustification
        fields = '__all__'


class CompetitveBidForm(forms.ModelForm):

    class Meta:
        model = CompetitiveBid
        fields = '__all__'
