from django.utils import timezone
from .models import Election
import logging

logger = logging.getLogger(__name__)

def update_elections():
    # Get the current time and date
    current_datetime = timezone.now()

    # Filter elections that are not ended and check their stop time
    elections = Election.objects.filter(is_ended=False)

    for election in elections:
        logger.debug(f"Checking election: {election.id}, stop_time: {election.stop_time}, current_time: {current_datetime}")
        
        # Compare the current datetime with the stop time of the election
        if election.stop_time <= current_datetime:
            winners_list = []
            
            # Group contestants by position
            positions = election.contestants.values_list('position', flat=True).distinct()

            for position in positions:
                contestants = election.contestants.filter(position=position)

                # Ensure that there are contestants for the position
                if contestants.exists():
                    # Get the contestant with the highest votes for each position
                    winner = contestants.order_by('-votes').first()
                    if winner:
                        winners_list.append({
                            'position': winner.position.name,  # Assuming position has a name field
                            'contestant': winner.name,
                            'votes': winner.votes
                        })

            # If winners were found, save them
            if winners_list:
                logger.debug(f"Election {election.id} has winners: {winners_list}")
                election.winners = winners_list
                election.is_ended = True  # Mark the election as ended
                election.save()  # Save the changes
                logger.debug(f"Election {election.id} marked as ended.")
            else:
                logger.debug(f"No winners found for election {election.id}.")
        else:
            logger.debug(f"Election {election.id} is still ongoing.")



