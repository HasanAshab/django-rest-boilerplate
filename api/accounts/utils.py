from api.common.utils import send_mail, client_route
from .tokens import verification_token


def send_verification_mail(user):
    token = verification_token.make_token(user)
    url = client_route.reverse('email-verification', {
      'id': user.id,
      'token': token
    })
    template = {
        'path': 'email/verification.html',
        'context': {'url': url}
    }
    send_mail(
        user=user,
        subject='Verify Email Address!',
        template=template
    )