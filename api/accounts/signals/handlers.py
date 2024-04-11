from django.dispatch import receiver
from api.accounts.utils import send_verification_mail
from api.accounts.signals import registered


@receiver(registered, dispatch_uid="send_email_verification_mail")
def send_email_verification_mail(sender, **kwargs):
    user = kwargs.get('user')
    if user and not user.is_email_verified:
        send_verification_mail(user)