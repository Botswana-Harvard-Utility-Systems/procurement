from django.apps import apps as django_apps


class RequestApprovalHelper(object):

    def __init__(self, request_approval, request_to, request_reason, status):
        self.request_approval = request_approval
        self.request_to = request_to
        self.request_reason = request_reason
        self.status = status

    @property
    def approved(self):
        approved = False
        if self.purchase_requisition:
            approved = self.check_prf_approval()
        elif self.purchase_order:
            approved = self.check_first_auth() or self.check_second_auth() or self.check_execute_approval()
        return approved

    def check_prf_approval(self):
        if self.status == 'approved':
            if self.request_reason == 'executive_approval':
                return True
            if self.check_second_request():
                return True
        return False

    def check_second_request(self):
        request = self.request()
        if request and request.status == 'approved':
            return True
        return False

    def check_funds_approval(self):
        if self.validation_required():
            if self.request_reason == 'confirm_funds' and self.status == 'approved':
                status = self.request.status if self.request else None
                if status and status == 'approved':
                    return True
                else:
                    return False
        return False

    def validation_required(self):
        val_required = False
        purchase_requisition = self.purchase_requisition
        if self.purchase_order:
            requisition_cls = django_apps.get_model('procurement.purchaserequisition')
            purchase_requisition = requisition_cls.objects.filter(
                prf_number=self.purchase_order.prf_number)[0]
        if purchase_requisition:
            total_cost = 0
            for item in purchase_requisition.purchaserequisitionitem_set.all():
                total_cost += item.total_price_incl
            if total_cost > 5000.0:
                val_required = True
        return val_required

    def check_first_auth(self):
        if self.request_reason == 'po_auth_one' and self.status == 'approved':
            if self.validation_required():
                status = self.request.status if self.request else None
                if status and status == 'approved':
                    return True
                else:
                    return False
            return True

    def check_second_auth(self):
        if self.validation_required():
            if self.request_reason == 'po_auth_two' and self.status == 'approved':
                status = self.request.status if self.request else None
                if status and status == 'approved':
                    return True
                else:
                    return False
        return False

    def check_execute_approval(self):
        if self.request_reason == 'executive_approval' and self.status == 'approved':
                return True
        return False

    @property
    def purchase_requisition(self):
        requisition_cls = django_apps.get_model('procurement.purchaserequisition')
        try:
            requisiton_obj = requisition_cls.objects.get(
                prf_number=self.request_approval.document_id)
        except requisition_cls.DoesNotExist:
            return None
        else:
            return requisiton_obj

    @property
    def purchase_order(self):
        order_cls = django_apps.get_model('procurement.purchaseorder')
        try:
            order_obj = order_cls.objects.get(
                order_number=self.request_approval.document_id)
        except order_cls.DoesNotExist:
            return None
        else:
            return order_obj

    @property
    def request(self):
        request_cls = django_apps.get_model('procurement.request')
        request_obj = request_cls.objects.filter(
            request_approval=self.request_approval).exclude(
                request_to=self.request_to, request_reason=self.request_reason)
        if request_obj:
            return request_obj.first()
        else:
            None
