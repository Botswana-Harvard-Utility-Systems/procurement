from django.contrib import admin

from ..admin_site import procurement_admin
from ..models import ProxyUser


@admin.register(ProxyUser, site=procurement_admin)
class ProxyUserAdmin(admin.ModelAdmin):

    search_fields = ['username', 'first_name', 'last_name', ]
