from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import CompanyForm
from ..models import Company


@admin.register(Company, site=procurement_admin)
class CompanyAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CompanyForm

    fieldsets = (
        (None, {
            'fields': ('tax_registration',
                       'name',
                       'address',),
        }),
        audit_fieldset_tuple)

    search_fields = ['tax_registration', 'name', ]
