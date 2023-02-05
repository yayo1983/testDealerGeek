from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import os


def send_user_mail(email, id):
    try:
        subject = 'Correo de aviso de paquete arrivado'
        template = get_template(os.path.join(settings.BASE_DIR, 'Templates/email_template.html'))
        content = template.render({
            'email': email,
            'id': id
        })

        message = EmailMultiAlternatives(subject=subject, body='', from_email=settings.EMAIL_HOST_USER, to=[email])
        message.attach_alternative(content, 'text/html')
        message.send()
        return True
    except:
        return False

