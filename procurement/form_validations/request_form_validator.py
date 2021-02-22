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

    @property
    def employee_model_cls(self):
        return django_apps.get_model('bhp_personnel.employee')

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

        self.validate_funds_confirmation()

        self.check_new_or_pending_request(request_approval)

        self.check_request_reason(request_approval, request_reason)

        self.check_approved_request(request_approval, request_to)

    def check_new_or_pending_request(self, request_approval):
        if self.add_form:
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

    def check_request_reason(self, request_approval, reason):
        if self.add_form:
            try:
                self.request_model_cls.objects.get(
                    request_approval=request_approval,
                    request_reason=reason)
            except self.request_model_cls.DoesNotExist:
                pass
            else:
                msg = {'request_reason':
                       f'Request for {reason} has already been posted.'}
                self._errors.update(msg)
                raise ValidationError(msg)

        if reason in ['po_auth_one', 'po_auth_two']:
            self.purchase_order_exists()
        elif reason in ['prf_approval', 'confirm_funds']:
            self.purchase_requisition_exists()

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

    def validate_funds_confirmation(self):
        cleaned_data = self.cleaned_data
        request_to = cleaned_data.get('request_to')
        request_reason = cleaned_data.get('request_reason')
        if request_reason and request_reason == 'confirm_funds':
            try:
                employee = self.employee_model_cls.objects.get(
                    email=request_to.email)
            except self.employee_model_cls.DoesNotExist:
                msg = {'request_to':
                       'Selected user does not exist as an employee. '
                       'Contact the system administrator for assistance.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            else:
                if employee.department.dept_name != 'Finance':
                    msg = {'request_to':
                           'Please select someone from finance to confirm availability of funds.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

    def purchase_order_exists(self):
        cleaned_data = self.cleaned_data
        purchase_order_model_cls = django_apps.get_model('procurement.purchaseorder')
        try:
            purchase_order_model_cls.objects.get(
                order_number=cleaned_data.get('request_approval').document_id)
        except purchase_order_model_cls.DoesNotExist:
            raise ValidationError('This is not a purchase order request.')
        else:
            pass

    def purchase_requisition_exists(self):
        cleaned_data = self.cleaned_data
        prf_model_cls = django_apps.get_model('procurement.purchaserequisition')
        try:
            prf_model_cls.objects.get(
                prf_number=cleaned_data.get('request_approval').document_id)
        except prf_model_cls.DoesNotExist:
            raise ValidationError('This is not a Purchase requisition request.')
        else:
            pass
