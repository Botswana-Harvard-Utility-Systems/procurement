from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import InvoiceForm, InvoiceItemForm
from ..models import Invoice, InvoiceItem


class InvoiceItemAdmin(TabularInlineMixin, admin.TabularInline):
    model = InvoiceItem
    form = InvoiceItemForm
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


@admin.register(Invoice, site=procurement_admin)
class InvoiceAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InvoiceForm
    inlines = [InvoiceItemAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('invoice_number',
                       'invoice_date',
                       'company',
                       'sales_rep',
                       'order_number',
                       'customer',),
        }),
        audit_fieldset_tuple)

    search_fields = ['invoice_number', 'sales_rep', 'order_number', ]

    autocomplete_fields = ['company', 'customer', ]
