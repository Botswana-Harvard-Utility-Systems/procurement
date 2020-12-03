from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import PurchaseOrderForm, PurchaseOrderItemForm
from ..models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderItemAdmin(TabularInlineMixin, admin.TabularInline):
    model = PurchaseOrderItem
    form = PurchaseOrderItemForm
    extra = 1

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


@admin.register(PurchaseOrder, site=procurement_admin)
class PurchaseOrderAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PurchaseOrderForm
    inlines = [PurchaseOrderItemAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('order_number',
                       'prf_number',
                       'order_date',
                       'agent',
                       'company',
                       'vendor',
                       'bhp_allocation',),
        }),
        audit_fieldset_tuple)

    search_fields = ['order_number', 'vendor', 'bhp_allocation', ]

    autocomplete_fields = ['company', 'bhp_allocation', 'vendor']
