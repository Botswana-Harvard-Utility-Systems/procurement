from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import VendorJustificationForm, CompetitveBidForm
from ..models import VendorJustification, CompetitiveBid


class CompetitiveBidAdmin(TabularInlineMixin, admin.TabularInline):
    model = CompetitiveBid
    form = CompetitveBidForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'vendor',
                'bid_price'
            )}),
        )

    autocomplete_fields = ['vendor', ]


@admin.register(VendorJustification, site=procurement_admin)
class VendorJustificationAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = VendorJustificationForm
    inlines = [CompetitiveBidAdmin]

    fieldsets = (
        ('Section A', {
            'fields': ('justification_number',
                       'prf_number',
                       'date',
                       'selected_vendor',
                       'not_lowest_bid',
                       'selected_source_explain',
                       'sole_source_explain',
                       'cost_analysis',
                       'voucher_no',
                       'cost_analysis_other'),
        }),
        audit_fieldset_tuple)

    search_fields = ['justification_number', 'prf_number', 'selected_vendor', ]

    autocomplete_fields = ['selected_vendor', ]

    filter_horizontal = ('cost_analysis', )

    radio_fields = {'not_lowest_bid': admin.VERTICAL, }
