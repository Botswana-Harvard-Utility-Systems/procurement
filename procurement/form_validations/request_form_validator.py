from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .form_calculations_mixin import FormCalculationsMixin


class RequestFormValidator(FormCalculationsMixin, FormValidator):

    @property
    def request_model_cls(self):
        return django_apps.get_model('procurement.request')

    @property
    def vendor_justification_model_cls(self):
        return django_apps.get_model('procurement.vendorjustification')

    def clean(self):
        request_approval = self.cleaned_data.get('request_approval')
        request_to = self.cleaned_data.get('request_to')

        prf_number = request_approval.document_id

        if request_approval:
            request_by = request_approval.request_by

            if request_to and request_to == request_by:
                msg = {'request_to':
                       'The requesting individual can not be the same as the person approving.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            msg = {'request_approval': 'Please select request approval.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        request_reason = self.cleaned_data.get('request_reason')
        if request_reason and (request_reason == 'prf_approval'
                               or request_reason == 'confirm_funds'):
            self.check_justification_exists(prf_number)

        self.check_new_or_pending_request(request_approval)

        self.check_approved_request(request_approval, request_to)

        self.required_if(
            'rejected',
            field='status',
            field_required='comment')

    def check_new_or_pending_request(self, request_approval):
        qs = self.request_model_cls.objects.filter(
            request_approval=request_approval, status__in=['new', 'pending'])
        if qs and qs.count() > 1:
            msg = {'__all__':
                   'There is already a new or pending approval request for this purchase.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def check_approved_request(self, request_approval, request_to):
        try:
            self.request_model_cls.objects.get(
                request_approval=request_approval,
                request_to=request_to, status='approved')
        except self.request_model_cls.DoesNotExist:
            pass
        else:
            msg = {'__all__':
                   f'{request_to.first_name} {request_to.last_name} has already '
                   'approved a request for this purchase. If this is a second request, '
                   'Please forward it to a different individual.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def check_justification_exists(self, prf_number):
        total_costs = self.items_total_cost(prf_number)
        if total_costs > 5000.00:
            try:
                self.vendor_justification_model_cls.objects.get(
                    prf_number=prf_number)
            except self.vendor_justification_model_cls.DoesNotExist:
                msg = {'__all__':
                       f'Total cost incl. of vat is {total_costs}, a Vendor '
                       'Justification is required for this purchase. Please complete it first.'}
                self._errors.update(msg)
                raise ValidationError(msg)
