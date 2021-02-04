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
                'request_reason',
                'date_reviewed',
                'status',
                'comment', )}),
        )

    autocomplete_fields = ['request_to', ]

    radio_fields = {'request_reason': admin.VERTICAL}

    def render_change_form(self, request, context, *args, **kwargs):
        if context['adminform'].form.fields:
            context['adminform'].form.fields['request_approval'].queryset = \
                RequestApproval.objects.filter(id=request.GET.get('request_approval'))
        return super(RequestAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(RequestAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if request.GET.get('request_approval'):
            request_by = RequestApproval.objects.get(
                id=request.GET.get('request_approval')).request_by
            if get_user(request) == request_by:
                fields = ('status', 'date_reviewed', ) + fields
            else:
                fields = ('status', 'request_to', 'request_reason', 'date_reviewed', ) + fields
        return fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        request_by = RequestApproval.objects.get(
            id=request.GET.get('request_approval')).request_by
        if get_user(request).id == int(request.GET.get('request_to')):
            extra_context = {'review': True}
        if get_user(request) == request_by and request.GET.get('status') == 'rejected':
            extra_context = {'retry': True}
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if change:
            if request.POST.get('_approve'):
                obj.status = 'approved'
            elif request.POST.get('_reject'):
                obj.status = 'rejected'
            elif request.POST.get('_retry'):
                obj.status = 'pending'
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'approved':
            return False
        if ((obj and obj.status == 'rejected') and
                get_user(request).id != obj.request_approval.request_by.id):
            return False
        return True


#     def redirect_url(self, request, obj, post_url_continue=None):
#         redirect_url = super().redirect_url(
#             request, obj, post_url_continue=post_url_continue)
#         if request.GET.dict().get('next'):
#             url_name = request.GET.dict().get('next').split(',')[0]
#             attrs = request.GET.dict().get('next').split(',')[1:]
#             if 'order_number' in attrs:
#                 options = {attrs[attrs.index('order_number')]:
#                            request.GET.dict().get('order_number')}
#                 try:
#                     redirect_url = reverse(url_name, kwargs=options)
#                 except NoReverseMatch as e:
#                     raise ModelAdminNextUrlRedirectError(
#                         f'{e}. Got url_name={url_name}, kwargs={options}.')
#         return redirect_url


class RequestApprovalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RequestApprovalForm

    fieldsets = (
        (None, {
            'fields': ('document_id',
                       'request_by',),
        }),
        audit_fieldset_tuple)

    search_fields = ['document_id', 'request_by', ]
