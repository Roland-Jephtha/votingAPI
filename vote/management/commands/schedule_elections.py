# your_app/management/commands/schedule_elections.py
from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from vote.tasks import update_elections

class Command(BaseCommand):
    help = 'Schedule the update_elections task'

    def handle(self, *args, **kwargs):
        # Schedule the update_elections task to run every 5 minutes
        schedule(
            'vote.tasks.update_elections',
            name='Update Elections',
            schedule_type='I',  # Interval-based schedule
            minutes=1  # Adjust this to the desired interval
        )
        self.stdout.write(self.style.SUCCESS('Election update task scheduled!'))
