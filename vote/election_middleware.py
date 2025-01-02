import logging
from django.utils import timezone
from django.db.models import Max
from .models import Election, Contestant

# Set up a logger to capture middleware activity
logger = logging.getLogger(__name__)

class UpdateElectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current time (aware of timezone if Django is set to use it)
        current_time = timezone.localtime(timezone.now()).time()

        # Fetch all elections that are still active (not ended yet)
        elections = Election.objects.filter(is_ended=False)

        for election in elections:
            try:
                # Check if the stop_time has passed (compare current time with stop_time)
                if election.stop_time <= current_time:
                    winners_list = []

                    # Group contestants by position
                    positions = election.contestants.values_list('position', flat=True).distinct()

                    # Iterate over each position and find the contestant with the highest votes
                    for position in positions:
                        contestants = election.contestants.filter(position=position)

                        if contestants.exists():
                            # Get the contestant with the highest votes in this position
                            winner = contestants.order_by('-votes').first()
                            if winner:
                                # Add the winner for this position to the winners list
                                winners_list.append({
                                    'position': winner.position.name,  # Assuming position has a 'name' field
                                    'contestant': winner.name,
                                    'votes': winner.votes,
                                })

                    # Update the election with the winners list and mark it as ended
                    election.winners = winners_list
                    election.is_ended = True
                    election.save()

                    logger.info(f"Election {election.id} has ended, winners have been updated.")
            except Exception as e:
                # Log any errors that occur during the process
                logger.error(f"Error processing election {election.id}: {str(e)}")

        # Process the request as normal
        response = self.get_response(request)
        return response
