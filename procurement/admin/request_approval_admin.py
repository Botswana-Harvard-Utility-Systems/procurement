from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import RequestApprovalForm
from ..models import RequestApproval


@admin.register(RequestApproval, site=procurement_admin)
class RequestApprovalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RequestApprovalForm

    fieldsets = (
        (None, {
            'fields': ('rfa_number',
                       'prf_number',
                       'request_by',
                       'request_to',
                       'approval_sign'),
        }),
        audit_fieldset_tuple)

    search_fields = ['rfa_number', 'request_by', 'request_to', ]
