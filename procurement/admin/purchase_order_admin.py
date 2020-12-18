from django.contrib.auth.models import User
from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import PurchaseOrderForm
from ..models import PurchaseOrder, PurchaseOrderMixin


@admin.register(PurchaseOrder, site=procurement_admin)
class PurchaseOrderAdmin(ModelAdminMixin, admin.ModelAdmin):

    extra_context_models = ['purchaserequisition', 'vendorjustification']

    form = PurchaseOrderForm

    fieldsets = (
        (None, {
            'fields': ('order_number',
                       'prf_number',
                       'order_date',
                       'agent',
                       'company', ),
        }),
        audit_fieldset_tuple)

    search_fields = ['order_number', ]

    autocomplete_fields = ['company', ]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['agent'].queryset = \
            User.objects.filter(groups__name='Procurement')
        return super(PurchaseOrderAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {}
        if self.extra_context_models:
            extra_context_dict = PurchaseOrderMixin(
                prf_number=request.GET.get('prf_number')).purchase_order_dict
            [extra_context.update({key: extra_context_dict.get(key)}) for key in self.extra_context_models]
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {}
        if self.extra_context_models:
            extra_context_dict = PurchaseOrderMixin(
                prf_number=request.GET.get('prf_number')).purchase_order_dict
            [extra_context.update({key: extra_context_dict.get(key)}) for key in self.extra_context_models]
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)
