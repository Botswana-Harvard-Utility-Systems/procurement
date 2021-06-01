from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'procurement'
    verbose_name = 'Procurement'
    admin_site_name = 'procurement_admin'
