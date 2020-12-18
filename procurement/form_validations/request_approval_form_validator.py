from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .form_calculations_mixin import FormCalculationsMixin


class RequestApprovalFormValidator(FormCalculationsMixin, FormValidator):

    @property
    def vendor_justification_cls(self):
        return django_apps.get_model('procurement.vendorjustification')

    def clean(self):
        self.validate_vendor_justification_exists()

    def validate_vendor_justification_exists(self):
        prf_number = self.cleaned_data.get('document_id')

        total_cost_accum = self.items_total_cost(prf_number)
        if total_cost_accum > 5000.00:
            self.check_vendor_justification_form(prf_number, total_cost_accum)

    def check_vendor_justification_form(self, prf_number, cost):
        try:
            self.vendor_justification_cls.objects.get(
                prf_number=prf_number)
        except self.vendor_justification_cls.DoesNotExist:
            raise ValidationError(
                f'Total cost for items is {cost}. Please complete the vendor '
                'justification form before requesting for any approvals.')
