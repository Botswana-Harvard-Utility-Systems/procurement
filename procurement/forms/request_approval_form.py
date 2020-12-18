from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..form_validations import RequestFormValidator, RequestApprovalFormValidator
from ..models import RequestApproval, Request, ProxyUser


class RequestApprovalForm(FormValidatorMixin, SiteModelFormMixin, forms.ModelForm):

    form_validator_cls = RequestApprovalFormValidator

    document_id = forms.CharField(
        label='Document Id',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = super().clean()
        requested_by = cleaned_data.get('request_by')

        if not self.data.get('request_set-0-request_to'):
            msg = {'__all__':
                   'Please complete a request for approval on the below table.'}
            raise forms.ValidationError(msg)
        else:
            requests = self.data.get('request_set-TOTAL_FORMS')
            for num in range(int(requests)):
                request_to = self.get_request_to(
                    self.data.get(f'request_set-{num}-request_to'))
                if requested_by == request_to:
                    msg = {'request_by':
                           'The requesting individual can not be the same as the person approving.'}
                    raise forms.ValidationError(msg)

    def get_request_to(self, user_id):
        try:
            user = ProxyUser.objects.get(id=user_id)
        except ProxyUser.DoesNotExist:
            pass
        else:
            return user

    class Meta:
        model = RequestApproval
        fields = '__all__'


class RequestForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = RequestFormValidator

    class Meta:
        model = Request
        fields = '__all__'
