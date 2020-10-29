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
    if not raw:
        if created:
            subject = (f'Approval Request for document no. {instance.document_id}')
            message = (f'Dear {instance.request_to.get_full_name()} \n\n Please note'
                       f' {instance.request_by} is requesting your approval for {instance.document_id}'
                       ' on the BHP Utility system https://bhp-utility-systems.bhp.org.bw. \n\n'
                       'Good day :).')
            from_email = 'adiphoko@bhp.org.bw'
            try:
                send_mail(
                    subject, message, from_email, [instance.request_to.email, ], fail_silently=False)
            except SMTPException as e:
                raise ValidationError(f'There was an error sending an email: {e}')
            else:
                RequestApproval.objects.filter(
                    rfa_number=instance.rfa_number).update(status='pending')
                Notifications.objects.create(
                    email=instance.request_to.email,
                    success_status=True)
