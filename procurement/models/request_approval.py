from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow

from .proxy_user import ProxyUser
from ..choices import DOC_STATUS, REQUEST_REASON


class RequestApproval(SiteModelMixin, BaseUuidModel):

    document_id = models.CharField(
        verbose_name='Document Id',
        max_length=50, )

    request_by = models.ForeignKey(ProxyUser, models.PROTECT)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.document_id}, {self.request_by}'

    class Meta:
        app_label = 'procurement'


class Request(BaseUuidModel):

    request_approval = models.ForeignKey(
        RequestApproval, on_delete=models.PROTECT)

    request_to = models.ForeignKey(ProxyUser, models.PROTECT)

    request_reason = models.CharField(
        max_length=100,
        choices=REQUEST_REASON)

    date_reviewed = models.DateField(default=get_utcnow)

    approval_sign = models.ImageField(
        verbose_name='Approval signature',
        upload_to='approval_signatures/',
        blank=True,
        null=True)

    status = models.CharField(
        max_length=8,
        choices=DOC_STATUS,
        default='new')

    comment = models.CharField(
        max_length=250,
        blank=True,
        null=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.id:
            self.request_approval.approved = self.approved
            self.request_approval.save()
        super().save(*args, **kwargs)

    @property
    def approved(self):
        approved = False
        if self.purchase_requisition:
            approved = self.check_prf_approval() or self.check_funds_approval()
        elif self.purchase_order:
            approved = self.check_first_auth() or self.check_second_auth()
        return approved

    def check_prf_approval(self):
        if self.request_reason == 'prf_approval' and self.status == 'approved':
            if self.validation_required():
                status = self.request.status if self.request else None
                if status and status == 'approved':
                    return True
                else:
                    return False
            return True

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

    class Meta:
        app_label = 'procurement'
        unique_together = ('request_approval', 'request_to', 'status')
        ordering = ('date_reviewed', )
