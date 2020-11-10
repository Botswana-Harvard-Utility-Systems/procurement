from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from smtplib import SMTPException

from bhp_personnel.models import Notifications
from .request_approval import RequestApproval


@receiver(post_save, weak=False, sender=RequestApproval,
          dispatch_uid='request_approval_on_post_save')
def request_approval_on_post_save(sender, instance, raw, created, **kwargs):
    """
        Notify user of an approval request for documents.
    """
    subject = (f'Approval Request for document no. {instance.document_id}')
    if not raw:
        if created:
            message = (f'Dear {instance.request_to.get_full_name()} \n\n Please note'
                       f' {instance.request_by} is requesting your approval for {instance.document_id}'
                       ' on the BHP Utility system https://bhp-utility-systems.bhp.org.bw. \n\n'
                       'Good day :).')
            from_email = 'adiphoko@bhp.org.bw'
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[instance.request_to.email, ])

        elif instance.status == 'pending':
            message = (f'Dear {instance.request_by} \n\n Please be informed '
                       f'Document no. {instance.document_id} has been approved.')
            from_email = 'adiphoko@bhp.org.bw'
            send_email_notification(
                instance, subject=subject, message=message, from_email=from_email,
                to_emails=[instance.request_by.email, ])


def send_email_notification(
        instance, subject=None, message=None, from_email=None, to_emails=[]):
    try:
        send_mail(subject, message, from_email, to_emails, fail_silently=False)
    except SMTPException as e:
        raise ValidationError(f'There was an error sending an email: {e}')
    else:
        Notifications.objects.create(email=instance.request_to.email, success_status=True)
        if instance.status == 'new':
            RequestApproval.objects.filter(
                document_id=instance.document_id).update(status='pending')
        elif instance.status == 'pending':
            RequestApproval.objects.filter(
                document_id=instance.document_id).update(status='approved')
