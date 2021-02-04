from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import DeliveredItem
from ..models import GoodsReceivedNote


class GoodsReceivedNoteForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    order_number = forms.CharField(
        label='Order number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        super().clean()
        delivered_item = self.data.get('delivereditem_set-0-description')

        if not delivered_item:
            msg = {'__all__': 'Please complete delivered items table below.'}
            raise forms.ValidationError(msg)

    class Meta:
        model = GoodsReceivedNote
        fields = '__all__'


class DeliveredItemForm(forms.ModelForm):

    class Meta:
        model = DeliveredItem
        fields = '__all__'
