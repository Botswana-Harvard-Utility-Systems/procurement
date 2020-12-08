from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..choices import SPLIT, SOLE
from ..models import Allocation
from ..models import PurchaseRequisition, PurchaseRequisitionItem, Quotation


class PurchaseRequisitionForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

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

    def clean(self):
        cleaned_data = super().clean()
        bhp_allocations = self.data.get('allocation_set-TOTAL_FORMS')
        allocation_type = cleaned_data.get('allocation_type')

        if allocation_type and not self.data.get('allocation_set-0-bhp_allocation'):
            msg = {'allocation_type': 'Bhp allocation is required, please specify below.'}
            raise forms.ValidationError(msg)

        if allocation_type == SPLIT and int(bhp_allocations) < 2:
            msg = {'allocation_type':
                   ('Allocation type is split, but only one study was specified '
                    'for allocation. Please add more studies or change type to sole.')}
            raise forms.ValidationError(msg)
        elif allocation_type == SOLE and int(bhp_allocations) != 1:
            msg = {'allocation_type':
                   ('Please provide a single study for bhp allocation.')}
            raise forms.ValidationError(msg)

        self.check_split_studies(bhp_allocations)

        self.check_allocation_percentages(allocation_type, bhp_allocations)

        purchase_item = self.data.get('purchaserequisitionitem_set-0-description')

        if not purchase_item:
            msg = {'__all__': 'Please complete purchase requisition items table.'}
            raise forms.ValidationError(msg)

        quotations = self.data.get('quotation_set-0-id')
        if not quotations and len(self.files) == 0:
            msg = {'__all__': 'Quotations are required for a requisition, please provide them.'}
            raise forms.ValidationError(msg)

    def check_allocation_percentages(self, all_type, allocations_total):
        percentage = self.data.get('allocation_set-0-percentage')
        if all_type == SOLE and int(float(percentage)) != 100:
            msg = {'allocation_type':
                   'Funds are sourced from a single study, percentage should be 100%.'}
            raise forms.ValidationError(msg)
        elif all_type == SPLIT:
            percentage = 0
            for num in range(int(allocations_total)):
                set_field = f'allocation_set-{num}-percentage'
                percentage += int(float(self.data.get(set_field)))
            if percentage != 100:
                msg = {'allocation_type':
                       ('Percentage allocation across studies should sum to 100%, '
                        f'total provided is {percentage}%.')}
                raise forms.ValidationError(msg)

    def check_split_studies(self, allocations_total):
        set_of_studies = set()
        list_of_studies = []
        for num in range(int(allocations_total)):
            study_id = self.data.get(f'allocation_set-{num}-bhp_allocation')
            list_of_studies.append(study_id)
        for study in list_of_studies:
            if study in set_of_studies:
                msg = {'allocation_type':
                       'Duplicate study specified for allocation, please correct '
                       'this or use sole type at 100% if funds are sourced from single study'}
                raise forms.ValidationError(msg)
            else:
                set_of_studies.add(study)

    class Meta:
        model = PurchaseRequisition
        fields = '__all__'


class AllocationForm(forms.ModelForm):

    class Meta:
        model = Allocation
        fields = '__all__'


class PurchaseRequisitionItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseRequisitionItem
        fields = '__all__'


class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotation
        fields = '__all__'
