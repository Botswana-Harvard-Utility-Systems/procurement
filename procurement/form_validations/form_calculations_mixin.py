from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class FormCalculationsMixin:

    @property
    def prf_model_cls(self):
        return django_apps.get_model('procurement.purchaserequisition')

    def items_total_cost(self, prf_number):
        try:
            prf = self.prf_model_cls.objects.get(prf_number=prf_number)
        except self.prf_model_cls.DoesNotExist:
            raise ValidationError(
                f'Purchase Requisition form for PRF No. {prf_number} does not exist.')
        else:
            requisition_items = prf.purchaserequisitionitem_set.all()
            total_cost_accum = 0
            if requisition_items:
                for item in requisition_items:
                    total_cost_accum += item.total_price_incl
            return total_cost_accum
