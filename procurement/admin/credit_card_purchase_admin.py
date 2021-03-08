from django.contrib import admin
from django.contrib.auth import get_user
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import CreditCardPurchaseForm
from ..models import CreditCardPurchase


@admin.register(CreditCardPurchase, site=procurement_admin)
class CreditCardPurchaseAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CreditCardPurchaseForm

    fieldsets = (
        (None, {
            'fields': ('req_date',
                       'grant_chargeable',
                       'description',
                       'accomodation',
                       'card_paid_accomo',
                       'currency',
                       'total_amount',
                       'alt_provider',
                       'selected_vendor',
                       'checkout_copy',
                       'card_holder',
                       'request_by',
                       'approval_by'),
        }),
        audit_fieldset_tuple)

    radio_fields = {'accomodation': admin.VERTICAL,
                    'card_paid_accomo': admin.VERTICAL,
                    'alt_provider': admin.VERTICAL}

    search_fields = ['grant_chargeable__name', 'request_by', ]

    readonly_fields = ['request_by', 'approval_by', ]

    autocomplete_fields = ['grant_chargeable', ]

    def save_model(self, request, obj, form, change):
        if change:
            if request.POST.get('_approve'):
                obj.status = 'approved'
            elif request.POST.get('_reject'):
                obj.status = 'rejected'
            elif request.POST.get('_retry'):
                obj.status = 'pending'
        if not change:
            obj.request_by = get_user(request)
            if request.POST.get('_request'):
                obj.status = 'pending'
        obj.save()
        super().save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.GET.get('approved'):
            if get_user(request).id == int(request.GET.get('request_by')):
                extra_context = {'request': True}
            if get_user(request) == request.GET.get('approval_by'):
                extra_context = {'approve': True}
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
