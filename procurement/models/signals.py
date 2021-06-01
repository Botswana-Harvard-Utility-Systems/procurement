from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from smtplib import SMTPException

from bhp_personnel.models import Notifications
from .proxy_user import ProxyUser
from .purchase_order import PurchaseOrder
from .purchase_requisition import PurchaseRequisition
from .request_approval import Request, RequestApproval
from .signature import Signature


@receiver(post_save, weak=False, sender=PurchaseRequisition)
@receiver(post_save, weak=False, sender=PurchaseOrder)
def create_request_approval(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            if sender.__name__ == 'PurchaseRequisition':
                document_id = instance.prf_number
                request_by = instance.request_by
            else:
                document_id = instance.order_number
                request_by = get_prf_field(instance.prf_number, 'request_by')
            try:
                RequestApproval.objects.get(
                    document_id=document_id)
            except RequestApproval.DoesNotExist:
                RequestApproval.objects.create(
                    document_id=document_id,
                    request_by=request_by)


@receiver(post_save, weak=False, sender=RequestApproval,
          dispatch_uid='request_on_post_save')
def request_approval_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if instance.approved:
            if is_purchase_requisition(instance.document_id):
                subject = f'Preparation of PO for document no. {instance.document_id} request'
                users = ProxyUser.objects.filter(groups__name='Procurement')
                message = (f'Purchase requisition {instance.document_id} has been '
                           'approved and a PO can now be prepared. ')
                from_email = 'adiphoko@bhp.org.bw'
                to_emails = [user.email for user in users]
                send_email_notification(
                    instance, subject=subject, message=message, from_email=from_email,
                    to_emails=to_emails)
                update_prf_field(instance.document_id, 'approved', True)
            elif is_purchase_order(instance.document_id):
                subject = f'Purchase order authorization'
                message = (f'Purchase order {instance.document_id} has been '
                           'authorised. ')
                from_email = 'adiphoko@bhp.org.bw'
                send_email_notification(
                    instance, subject=subject, message=message, from_email=from_email,
                    to_emails=[instance.request_by.email, ])
                update_obj_field(
                    model_cls=PurchaseOrder, identifier_field='order_number',
                    identifier_value=instance.document_id,
                    field_name='authorised', value=True)


@receiver(post_save, weak=False, sender=Request,
          dispatch_uid='request_on_post_save')
def request_on_post_save(sender, instance, raw, created, **kwargs):
    """
        Notify user of an approval request for documents.
    """
    subject = (f'Approval Request for document no. {instance.request_approval.document_id}')
    if not raw:
        request_approval = instance.request_approval
        current_site = get_current_site(request=None)
        if created:
            message = (f'Dear {instance.request_to.get_full_name()} \n\n Please note'
                       f' {request_approval.request_by} is requesting your'
                       f' approval for {request_approval.document_id}'
                       f' on the BHP Utility system http://{current_site.domain}. \n\n'
                       'Good day :).')
            from_email = 'adiphoko@bhp.org.bw'
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[instance.request_to.email, ], status=instance.status)

        elif instance.status in ['approved', 'rejected']:
            message = (f'Dear {request_approval.request_by} \n\n Please be informed '
                       f'Document no. {request_approval.document_id} has been {instance.status}.'
                       f'Visit http://{current_site.domain} for further details.')
            from_email = 'adiphoko@bhp.org.bw'
            user = check_user(request_approval.request_by)
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[user.email, ], status=instance.status)

        elif instance.status == 'pending':
            message = (f'Dear {instance.request_to.get_full_name()} \n\n Please note'
                       f' {request_approval.request_by} is re-requesting your'
                       f' approval for {request_approval.document_id}'
                       f' on the BHP Utility system http://{current_site.domain}. \n\n'
                       'Good day :).')
            from_email = 'adiphoko@bhp.org.bw'
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[instance.request_to.email, ], status=instance.status)


def send_email_notification(
        instance, subject=None, message=None, from_email=None, to_emails=[], status=None):
    try:
        send_mail(subject, message, from_email, to_emails, fail_silently=False)
    except SMTPException as e:
        raise ValidationError(f'There was an error sending an email: {e}')
    else:
#         Notifications.objects.create(
#             email=instance.request_to.email, success_status=True)
        if status:
            if status == 'new':
                instance.status = 'pending'
                if instance.request_reason in 'prf_approval':
                    value = instance.request_to
                    update_prf_field(
                        prf_number=instance.request_approval.document_id, field_name='approval_by', value=value)
                elif instance.request_reason == 'confirm_funds':
                    value = instance.request_to
                    update_prf_field(
                        prf_number=instance.request_approval.document_id, field_name='funds_confirmed', value=value)
                elif instance.request_reason == 'po_auth_one':
                    value = instance.request_to
                    update_obj_field(
                        model_cls=PurchaseOrder, identifier_field='order_number',
                        identifier_value=instance.request_approval.document_id, field_name='first_approver', value=value)
                elif instance.request_reason == 'po_auth_two':
                    value = instance.request_to
                    update_obj_field(
                        model_cls=PurchaseOrder, identifier_field='order_number',
                        identifier_value=instance.request_approval.document_id, field_name='second_approver', value=value)
                elif instance.request_reason == 'executive_approval':
                    identifier = instance.request_approval.document_id
                    value = instance.request_to
                    if is_purchase_requisition(identifier):
                        update_obj_field(
                            model_cls=PurchaseRequisition, identifier_field='prf_number',
                            identifier_value=identifier, field_name='approval_by', value=value)
                    else:
                        update_obj_field(
                            model_cls=PurchaseOrder, identifier_field='order_number',
                            identifier_value=identifier, field_name='first_approver', value=value)
                instance.save()
            else:
                instance.status = status
                if instance.status == 'approved':
                    signature = user_signature(instance.request_to)
                    instance.approval_sign = signature


def check_user(user):
    if not isinstance(user, ProxyUser):
        try:
            return ProxyUser.objects.get(id=user.id)
        except ProxyUser.DoesNotExist:
            raise ValidationError(f'User does not exist.')
    return user


def update_prf_field(prf_number=None, field_name=None, value=None):
    try:
        prf = PurchaseRequisition.objects.get(prf_number=prf_number)
    except PurchaseRequisition.DoesNotExist:
        raise ValidationError('Purchase Requisition matching id does not exist')
    else:
        setattr(prf, field_name, value)
        prf.save()


def update_obj_field(model_cls=None, identifier_field=None,
                     identifier_value=None, field_name=None, value=None):
    try:
        model_obj = model_cls.objects.get(**{f'{identifier_field}': identifier_value})
    except model_cls.DoesNotExist:
        raise ValidationError(f'{model_cls} matching id does not exist')
    else:
        setattr(model_obj, field_name, value)
        model_obj.save()


def get_prf_field(prf_number=None, field_name=None):
    try:
        prf = PurchaseRequisition.objects.get(prf_number=prf_number)
    except PurchaseRequisition.DoesNotExist:
        raise ValidationError('Purchase Requisition matching id does not exist')
    else:
        return getattr(prf, field_name, None)


def user_signature(user):
    try:
        signature = Signature.objects.get(owner=user)
    except Signature.DoesNotExist:
        raise ValidationError(
            'Authorising person does not have signature captured, please '
            'contact admin for assistance on this.')
    else:
        return signature.signature


def is_purchase_requisition(prf_number):
    try:
        PurchaseRequisition.objects.get(prf_number=prf_number)
    except PurchaseRequisition.DoesNotExist:
        return False
    else:
        return True


def is_purchase_order(order_number):
    try:
        PurchaseOrder.objects.get(order_number=order_number)
    except PurchaseOrder.DoesNotExist:
        return False
    else:
        return True

