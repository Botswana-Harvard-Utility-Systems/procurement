from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import CustomerForm
from ..models import Customer


@admin.register(Customer, site=procurement_admin)
class CustomerAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CustomerForm

    fieldsets = (
        (None, {
            'fields': ('account_number',
                       'customer_ref',
                       'name',
                       'description',
                       'address',
                       'contact_person'),
        }),
        audit_fieldset_tuple)

    search_fields = ['account_number', 'customer_ref', 'name', ]

    autocomplete_fields = ['address', ]
