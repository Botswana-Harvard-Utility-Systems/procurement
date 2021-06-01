from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin, ModelAdminNextUrlRedirectError

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
            'fields': ('order_number',
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

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            options.pop('vendor')
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def save_model(self, request, obj, form, change):
        if not change:
            obj.received_by = request.user.username
        super().save_model(request, obj, form, change)
