from django.core.mail import send_mail
from django.conf import settings

def send_activation_pin(user):
    subject = 'Your Account Activation PIN'
    message = f"Hi {user.first_name},\n\nYour account activation PIN is: {user.pin}\n\nUse this PIN to activate your account."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
