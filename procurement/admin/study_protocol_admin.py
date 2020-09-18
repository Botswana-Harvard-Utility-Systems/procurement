from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import StudyProtocolForm
from ..models import StudyProtocol


@admin.register(StudyProtocol, site=procurement_admin)
class StudyProtocolAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = StudyProtocolForm

    fieldsets = (
        (None, {
            'fields': ('number',
                       'name', ),
        }),
        audit_fieldset_tuple)

    search_fields = ['number', 'name', ]
