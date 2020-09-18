from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import AddressForm
from ..models import Address


@admin.register(Address, site=procurement_admin)
class AddressAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = AddressForm

    fieldsets = (
        (None, {
            'fields': ('telephone_contacts',
                       'email',
                       'fax',
                       'physical_address',
                       'postal_address',),
        }),
        audit_fieldset_tuple)

    search_fields = ['email', 'telephone_contacts', ]
