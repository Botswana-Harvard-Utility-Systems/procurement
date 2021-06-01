from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import OTHER


class VendorJustificationFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            'selected_source',
            field='not_lowest_bid',
            field_required='selected_source_explain')

        self.required_if(
            'sole_source',
            field='not_lowest_bid',
            field_required='sole_source_explain')

        cost_analysis = self.cleaned_data.get('cost_analysis')
        selected = []

        for analysis in cost_analysis:
            selected.append(analysis.short_name)

        if 'compares_favorable' in selected and not self.cleaned_data.get('voucher_no'):
            msg = {'voucher_no': 'Please specify the voucher no.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        elif 'compares_favorable' not in selected and self.cleaned_data.get('voucher_no'):
            msg = {'voucher_no': 'This field is not required'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if OTHER in selected and not self.cleaned_data.get('cost_analysis_other'):
            msg = {'cost_analysis_other': 'Please specify other considerations.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        elif OTHER not in selected and self.cleaned_data.get('cost_analysis_other'):
            msg = {'cost_analysis_other': 'This field is not required'}
            self._errors.update(msg)
            raise ValidationError(msg)
