from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import DeliveredItemForm, GoodsReceivedNoteForm
from ..models import DeliveredItem
from ..models import GoodsReceivedNote


class DeliveredItemAdmin(TabularInlineMixin, admin.TabularInline):
    model = DeliveredItem
    form = DeliveredItemForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'description',
                'order_quantity',
                'delivered_quantity', )}),
        )


@admin.register(GoodsReceivedNote, site=procurement_admin)
class GoodsReceivedNoteAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = GoodsReceivedNoteForm
    inlines = [DeliveredItemAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('grn_number',
                       'order_number',
                       'vendor',
                       'date_received',
                       'delivery_note_attached',
                       'delivery_note',
                       'received_by',
                       'delivered_by', ),
        }),
        audit_fieldset_tuple)

    radio_fields = {'delivery_note_attached': admin.VERTICAL}

    search_fields = ['grn_number', 'order_number', 'vendor', ]

    readonly_fields = ['received_by', ]
