from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import CreditCardPurchase


class CreditCardPurchaseForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreditCardPurchaseForm, self).__init__(*args, **kwargs)
        self.fields['ccp_number'].required = False

    ccp_number = forms.CharField(
        label='Credit Card purchase number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CreditCardPurchase
        fields = '__all__'
