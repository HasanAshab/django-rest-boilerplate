from api.common.utils import send_mail


def send_verification_mail(user):
    url = 'jd'
    template = {
        'path': 'email/verification.html',
        'context': {'url': url}
    }
    send_mail(
        user=user,
        subject='Verify Email Address!',
        template=template
    )