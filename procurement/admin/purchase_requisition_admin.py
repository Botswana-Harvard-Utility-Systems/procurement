from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import StackedInlineMixin, TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import PurchaseRequisitionForm, PurchaseRequisitionItemForm
from ..forms import AllocationForm, QuotationForm
from ..models import Allocation
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


class AllocationAdmin(StackedInlineMixin, admin.StackedInline):
    model = Allocation
    form = AllocationForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'bhp_allocation',
                'percentage', )}),
        )

    autocomplete_fields = ['bhp_allocation', ]


@admin.register(PurchaseRequisition, site=procurement_admin)
class PurchaseRequisitionAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PurchaseRequisitionForm
    inlines = [AllocationAdmin, PurchaseRequisitionItemAdmin, QuotationAdmin]

    fieldsets = (
        (None, {
            'fields': ('prf_number',
                       'req_date',
                       'reason',
                       'allocation_type',
                       'approval_by',
                       'funds_confirmed',
                       'request_by',),
        }),
        audit_fieldset_tuple)

    radio_fields = {'allocation_type': admin.VERTICAL}

    search_fields = ['prf_number', 'request_by', ]

    readonly_fields = ['request_by', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.request_by = request.user
        obj.save()
