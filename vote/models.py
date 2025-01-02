from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
from datetime import datetime
from django.db.models import F


class Position(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name




class User_Data(models.Model):
    voters_id = models.CharField(max_length=13, blank=True, null=True)
    first_name = models.CharField(max_length=13, blank=True, null=True)
    last_name = models.CharField(max_length=13, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)  # Only one phone field
    email = models.EmailField(unique=True, null=True)
    matricnum = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    voted = models.ManyToManyField('Contestant', through='UserVote', blank=True)  # Linking to Contestant model
    approved = models.BooleanField(default=False)

    def generate_voters_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
    
    def __str__(self):
        return self.email



@receiver(post_save, sender=User_Data)
def send_voter_id_email(sender, instance, created, **kwargs):
    # Only send email if approved is set to True and it's a new instance or just updated to approved
    if instance.approved and ( not created or instance.approved != instance.__class__.objects.get(id=instance.id).approved):
        if not instance.voters_id:
            instance.voters_id = instance.generate_voters_id()
            instance.save(update_fields=['voters_id'])

        subject = "Your Voters ID"
        email_from = settings.EMAIL_HOST_USER
        message = f'Hello {instance.first_name}, your voters ID is: {instance.voters_id}'
        
        try:
            send_mail(subject, message, email_from, [instance.email], fail_silently=False)
        except Exception as e:
            print(f'Failed to send email: {str(e)}')  # Log error if needed





class UserVote(models.Model):
    user = models.ForeignKey(User_Data, on_delete=models.CASCADE)
    contestant = models.ForeignKey('Contestant', on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.email
    

@receiver(post_save, sender=UserVote)
def increment_contestant_votes(sender, instance, created, **kwargs):
    if created:  # Only increment if a new UserVote is created
        Contestant.objects.filter(id=instance.contestant.id).update(votes=F('votes') + 1)




class Contestant(models.Model):
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='contestant_images/', null=True, blank=True)  # Changed to ImageField
    position = models.ForeignKey('Position',on_delete=models.CASCADE, null = True)
    tagline = models.CharField(max_length=500, blank=True, null=True)
    votes = models.PositiveIntegerField(default=0, blank=True, null=True)
    contestant_id = models.CharField(max_length=20, unique=True, editable=False, null=True)  # ID generation

    def __str__(self):
        return self.name




from django.db import models
from django.utils import timezone
from datetime import timedelta

class Election(models.Model):
    start_time = models.TimeField()
    stop_time = models.TimeField()
    no_of_hours = models.PositiveIntegerField(editable=False)
    is_ended = models.BooleanField(default=False)
    contestants = models.ManyToManyField('Contestant')
    winners = models.JSONField(default=dict, blank=True, null=True)  # Allow null values
    position = models.ManyToManyField('Position', null=True)
    current_time = models.TimeField(null=True, blank=True)

    def clean(self):
        # Ensure start time is before stop time
        if self.start_time >= self.stop_time:
            # raise ValidationError("Start time must be before stop time.")
            pass

    def save(self, *args, **kwargs):
        # Use the server's current time
        now = datetime.now()

        # Manually adjust the time by subtracting 1 hour to sync with server time
        adjusted_now = now

        # Convert TimeField values (start_time and stop_time) into datetime objects
        start_datetime = adjusted_now.replace(hour=self.start_time.hour, minute=self.start_time.minute, second=self.start_time.second, microsecond=0)
        stop_datetime = adjusted_now.replace(hour=self.stop_time.hour, minute=self.stop_time.minute, second=self.stop_time.second, microsecond=0)

        # If stop_time is earlier in the day than start_time, it means the election runs overnight
        if stop_datetime < start_datetime:
            stop_datetime += timedelta(days=1)  # Adjust to the next day

        # Calculate the difference in seconds and convert to hours
        duration_in_seconds = (stop_datetime - start_datetime).total_seconds()
        self.no_of_hours = int(duration_in_seconds // 3600)  # Convert seconds to hours

        # Save the adjusted current time
        self.current_time = adjusted_now.time()

        super(Election, self).save(*args, **kwargs)

 


    def __str__(self):
        return f"Election from {self.start_time} to {self.stop_time}"
