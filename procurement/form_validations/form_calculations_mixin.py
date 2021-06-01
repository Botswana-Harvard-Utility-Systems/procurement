from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class FormCalculationsMixin:

    @property
    def prf_model_cls(self):
        return django_apps.get_model('procurement.purchaserequisition')

    @property
    def po_model_cls(self):
        return django_apps.get_model('procurement.purchaseorder')

    def is_purchase_order(self, order_number):
        try:
            po = self.po_model_cls.objects.get(order_number=order_number)
        except self.po_model_cls.DoesNotExist:
            return None
        else:
            return po

    def items_total_cost(self, prf_number):
        po = self.is_purchase_order(prf_number)
        if po:
            prf_number = po.prf_number

        try:
            prf = self.prf_model_cls.objects.get(prf_number=prf_number)
        except self.prf_model_cls.DoesNotExist:
            raise ValidationError(f'PRF for {prf_number} does not exist.')
        else:
            requisition_items = prf.purchaserequisitionitem_set.all()
            total_cost_accum = 0
            if requisition_items:
                for item in requisition_items:
                    total_cost_accum += item.total_price_incl
            return total_cost_accum
