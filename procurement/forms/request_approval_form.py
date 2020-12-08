from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import RequestApproval, Request, ProxyUser


class RequestApprovalForm(SiteModelFormMixin, forms.ModelForm):

    document_id = forms.CharField(
        label='Document Id',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = super().clean()
        requested_by = cleaned_data.get('requested_by')

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
                    msg = {'requested_by':
                           'The requesting individual can not be the same as the approver.'}
                    raise forms.ValidationError(msg)

    def get_request_to(self, user_id):
        try:
            user = ProxyUser.objects.get(id=user_id)
        except ProxyUser.DoesNotExist:
            raise forms.ValidationError('User requested does not exist.')
        else:
            return user

    class Meta:
        model = RequestApproval
        fields = '__all__'


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = '__all__'
