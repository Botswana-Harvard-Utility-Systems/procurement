from django.contrib import admin

from ..admin_site import procurement_admin
from ..forms import SignatureForm
from ..models import Signature


@admin.register(Signature, site=procurement_admin)
class SignatureAdmin(admin.ModelAdmin):

    form = SignatureForm

    fieldsets = (
        (None, {
            'fields': (
                'owner',
                'signature', )}),
        )

    autocomplete_fields = ['owner', ]
