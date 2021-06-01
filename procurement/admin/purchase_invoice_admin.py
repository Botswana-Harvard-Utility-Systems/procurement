from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import ModelAdminNextUrlRedirectError
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import procurement_admin
from ..forms import PurchaseInvoiceForm
from ..models import PurchaseInvoice, Supplier


@admin.register(PurchaseInvoice, site=procurement_admin)
class PurchaseInvoiceAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PurchaseInvoiceForm

    fieldsets = (
        (None, {
            'fields': ('invoice_number',
                       'order_number',
                       'invoice_date',
                       'vendor',
                       'company',
                       'paid',
                       'document',),
        }),
        audit_fieldset_tuple)

    search_fields = ['invoice_number', 'vendor__name', ]

    autocomplete_fields = ['company', ]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return ('paid', ) + fields

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {attrs[attrs.index('order_number')]:
                       request.GET.dict().get('order_number')}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

#     def render_change_form(self, request, context, *args, **kwargs):
#         if context['adminform'].form.fields:
#             context['adminform'].form.fields['vendor'].queryset = \
#                 Supplier.objects.filter(id=request.GET.get('vendor'))
#         return super(PurchaseInvoiceAdmin, self).render_change_form(
#             request, context, *args, **kwargs)
