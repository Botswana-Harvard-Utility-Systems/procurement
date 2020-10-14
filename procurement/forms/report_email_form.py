from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import ReportEmail


class ReportEmailForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = ReportEmail
        fields = ['sender_email', 'receipient_email', 'subject', 'message']
        labels = {
            'sender_email': 'From',
            'receipient_email': 'To', }
