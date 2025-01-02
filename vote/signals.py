# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User_Data



@receiver(post_save, sender=User_Data)
def send_voters_id_email(sender, instance, created, **kwargs):
    # Check if it's an update (not a creation) and approved is True
    if not created and instance.approved:
        email = instance.email
        subject = "Your Voters ID"
        message = f'Hello {instance.first_name}, your voters ID is: {instance.voters_id}'
        email_from = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, email_from, [email], fail_silently=False)
        except Exception as e:
            print(f"Error sending email: {e}")  # You may also log this error




    # elif created and instance.approved:
    #     email = instance.email
    #     subject = "Your Voters ID"
    #     message = f'Hello {instance.first_name}, your voters ID is: {instance.voters_id}'
    #     email_from = settings.EMAIL_HOST_USER

    #     try:
    #         send_mail(subject, message, email_from, [email], fail_silently=False)
    #     except Exception as e:
    #         print(f"Error sending email: {e}")  # You may also log this error




