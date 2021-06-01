from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import SupplierForm
from ..models import Supplier


@admin.register(Supplier, site=procurement_admin)
class SupplierAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SupplierForm

    fieldsets = (
        (None, {
            'fields': ('supplier_identifier',
                       'supplier',
                       'name',
                       'description',
                       'address',
                       'contact_person',
                       'supplier_locality',
                       'supplier_group',
                       'currency',),
        }),
        audit_fieldset_tuple)

    radio_fields = {
        'supplier_locality': admin.VERTICAL,
        'supplier_group': admin.VERTICAL,
        'currency': admin.VERTICAL, }

    search_fields = ['supplier', 'name', 'contact_person', 'supplier_group']

    autocomplete_fields = ['address', ]
