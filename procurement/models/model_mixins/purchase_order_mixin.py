from django.apps import apps as django_apps


class PurchaseOrderMixin:

    def __init__(self, prf_number=None):
        self.prf_number = prf_number
        self.purchase_order_dict = {}
        self.purchase_order_dict.update(self.order_dict)

    @property
    def order_dict(self):
        model_cls_list = ['procurement.purchaserequisition',
                          'procurement.vendorjustification']

        object_dict = {}
        for model in model_cls_list:
            model_cls = django_apps.get_model(model)
            try:
                model_obj = model_cls.objects.get(prf_number=self.prf_number)
            except model_cls.DoesNotExist:
                pass
            else:
                object_dict.update({model.split(".")[1]: model_obj})
        return object_dict
