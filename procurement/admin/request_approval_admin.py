from django.contrib.auth import get_user
from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import RequestApprovalForm, RequestForm
from ..models import RequestApproval, Request


@admin.register(Request, site=procurement_admin)
class RequestAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RequestForm

    fieldsets = (
        (None, {
            'fields': (
                'request_approval',
                'request_to',
                'date_reviewed',
                'status',
                'comment', )}),
        )

    autocomplete_fields = ['request_to', ]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if request.GET.get('request_approval'):
            request_by = RequestApproval.objects.get(
                id=request.GET.get('request_approval')).request_by
            if get_user(request) == request_by:
                fields = ('status', ) + fields

        return fields


@admin.register(RequestApproval, site=procurement_admin)
class RequestApprovalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RequestApprovalForm

    fieldsets = (
        (None, {
            'fields': ('document_id',
                       'request_by',),
        }),
        audit_fieldset_tuple)

    search_fields = ['document_id', 'request_by', ]
