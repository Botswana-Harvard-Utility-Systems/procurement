from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import PurchaseRequisitionForm, PurchaseRequisitionItemForm
from ..forms import QuotationForm
from ..models import PurchaseRequisition, PurchaseRequisitionItem, Quotation


class PurchaseRequisitionItemAdmin(TabularInlineMixin, admin.TabularInline):
    model = PurchaseRequisitionItem
    form = PurchaseRequisitionItemForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'description',
                'item_code',
                'quantity_ordered',
                'unit_price',
                'total_price_excl',
                'vat',
                'total_price_incl', )}),
        )


class QuotationAdmin(TabularInlineMixin, admin.TabularInline):
    model = Quotation
    form = QuotationForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'quotes', )}),
        )


@admin.register(PurchaseRequisition, site=procurement_admin)
class PurchaseRequisitionAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PurchaseRequisitionForm
    inlines = [PurchaseRequisitionItemAdmin, QuotationAdmin]

    fieldsets = (
        (None, {
            'fields': ('prf_number',
                       'req_date',
                       'bhp_allocation',
                       'reason',
                       'approval_by',
                       'funds_confirmed',
                       'request_by',),
        }),
        audit_fieldset_tuple)

    search_fields = ['prf_number', 'bhp_allocation', 'request_by', ]

    autocomplete_fields = ['bhp_allocation', ]

    readonly_fields = ['request_by', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.request_by = request.user
        obj.save()
