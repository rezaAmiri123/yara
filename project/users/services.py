from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


def send_email_token(email, token):
    message = _('your registration token is %s' % token)
    send_mail(
        subject=_('email validation'),
        message=message,
        from_email='admin@example.com',
        recipient_list=[email]
    )
