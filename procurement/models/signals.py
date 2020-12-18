from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from smtplib import SMTPException

from bhp_personnel.models import Notifications
from .proxy_user import ProxyUser
from .purchase_requisition import PurchaseRequisition
from .request_approval import Request, RequestApproval


@receiver(post_save, weak=False, sender=PurchaseRequisition)
def create_request_approval(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            try:
                RequestApproval.objects.get(
                    document_id=instance.prf_number)
            except RequestApproval.DoesNotExist:
                RequestApproval.objects.create(
                    document_id=instance.prf_number,
                    request_by=instance.request_by)


@receiver(post_save, weak=False, sender=Request,
          dispatch_uid='request_on_post_save')
def request_on_post_save(sender, instance, raw, created, **kwargs):
    """
        Notify user of an approval request for documents.
    """
    subject = (f'Approval Request for document no. {instance.request_approval.document_id}')
    if not raw:
        request_approval = instance.request_approval
        if created:
            message = (f'Dear {instance.request_to.get_full_name()} \n\n Please note'
                       f' {request_approval.request_by} is requesting your'
                       f' approval for {request_approval.document_id}'
                       ' on the BHP Utility system https://bhp-utility-systems.bhp.org.bw. \n\n'
                       'Good day :).')
            from_email = 'adiphoko@bhp.org.bw'
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[instance.request_to.email, ], status=instance.status)

        elif instance.status == 'approved':
            message = (f'Dear {request_approval.request_by} \n\n Please be informed '
                       f'Document no. {request_approval.document_id} has been approved.')
            from_email = 'adiphoko@bhp.org.bw'
            user = check_user(request_approval.request_by)
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[user.email, ], status=instance.status)


def send_email_notification(
        instance, subject=None, message=None, from_email=None, to_emails=[], status=None):
    try:
        send_mail(subject, message, from_email, to_emails, fail_silently=False)
    except SMTPException as e:
        raise ValidationError(f'There was an error sending an email: {e}')
    else:
        Notifications.objects.create(
            email=instance.request_to.email, success_status=True)
        if status == 'new':
            value = f'{instance.request_to.first_name} {instance.request_to.last_name}'
            instance.status = 'pending'
            instance.save()
            update_prf_field(
                prf_number=instance.request_approval.document_id, field_name='approval_by', value=value)
        elif status == 'approved':
            update_prf_field(
                prf_number=instance.request_approval.document_id, field_name='approved',
                value=True)


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
