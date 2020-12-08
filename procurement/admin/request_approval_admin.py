from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import RequestApprovalForm, RequestForm
from ..models import RequestApproval, Request, ProxyUser


class RequestAdmin(TabularInlineMixin, admin.TabularInline):
    model = Request
    form = RequestForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'request_to',
                'date_reviewed',
                'status',
                'comment', )}),
        )

    autocomplete_fields = ['request_to', ]


@admin.register(RequestApproval, site=procurement_admin)
class RequestApprovalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RequestApprovalForm

    inlines = [RequestAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('document_id',
                       'request_by',),
        }),
        audit_fieldset_tuple)

    search_fields = ['document_id', 'request_by', ]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['request_by'].queryset = \
            ProxyUser.objects.filter(id=request.GET.get('request_by'))
        return super(RequestApprovalAdmin, self).render_change_form(
            request, context, *args, **kwargs)
