from django.contrib import admin
from django.contrib.auth import get_user
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
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'description',
                'item_code',
                'quantity_ordered',
                'unit_price',
                'discount',
                'total_price_excl',
                'vat',
                'total_price_incl', )}),
        )


class QuotationAdmin(TabularInlineMixin, admin.TabularInline):
    model = Quotation
    form = QuotationForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'quotes', )}),
        )


class AllocationAdmin(StackedInlineMixin, admin.StackedInline):
    model = Allocation
    form = AllocationForm
    extra = 0

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
                       'selected_vendor',
                       'request_by',
                       'approval_by',
                       'funds_confirmed',),
        }),
        audit_fieldset_tuple)

    radio_fields = {'allocation_type': admin.VERTICAL}

    search_fields = ['prf_number', 'request_by', ]

    readonly_fields = ['request_by', 'approval_by', 'funds_confirmed', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.request_by = get_user(request)
        obj.save()
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        user_created = obj.user_created if obj else None
        approved = obj.approved if obj else False
        if user_created and user_created != get_user(request).username:
            return False
        if approved:
            return False
        return True
