# from functools import wraps
# from django.utils import timezone
# from .models import Election, Position, Contestant
# from django.db.models import Count

# def calculate_winners_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         election_id = kwargs.get('election_id')  # Ensure you pass election_id to the view
#         try:
#             election = Election.objects.get(id=election_id)

#             # Check if the stop_time has passed and is_ended is False
#             if election.stop_time <= timezone.now().time() and not election.is_ended:
#                 election.is_ended = True  # Set the election as ended
#                 winners = {}

#                 # Calculate winners for each position
#                 positions = Position.objects.all()
#                 for position in positions:
#                     winner = Contestant.objects.filter(position=position) \
#                         .annotate(vote_count=Count('uservote')) \
#                         .order_by('-vote_count').first()

#                     if winner:
#                         winners[position.name] = {
#                             'winner_id': winner.id,
#                             'winner_name': winner.name,
#                             'votes': winner.vote_count
#                         }
#                     else:
#                         winners[position.name] = {
#                             'winner_id': None,
#                             'winner_name': "No votes",
#                             'votes': 0
#                         }

#                 # Save winners and mark the election as ended
#                 election.winners = winners
#                 election.save()

#             # Proceed with the original view logic
#             return func(*args, **kwargs)

#         except Election.DoesNotExist:
#             return None  # Handle the case where the election does not exist

#     return wrapper





















































from rest_framework.response import Response
from rest_framework import status
from .models import Election
from functools import wraps
from django.utils import timezone  # To get the current time

def calculate_winners_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(self, *args, **kwargs):
        # Call the original view function and store the response
        response = view_func(self, *args, **kwargs)

        # Check if the response is a successful election creation (HTTP 201)
        if response.status_code == status.HTTP_201_CREATED:
            election_id = response.data.get('data', {}).get('id')  # Adjust to match your response structure

            if election_id:
                try:
                    # Retrieve the election instance by the ID
                    election_instance = Election.objects.get(id=election_id)

                    # Check if the current time has passed the stop_time of the election
                    current_time = timezone.now()
                    if current_time >= election_instance.stop_time:
                        winners_list = []

                        # Group contestants by position
                        positions = election_instance.contestants.values_list('position', flat=True).distinct()

                        for position in positions:
                            # Get contestants for each position
                            contestants = election_instance.contestants.filter(position=position)
                            
                            if contestants.exists():
                                # Find the contestant with the maximum votes for the position
                                winner = contestants.order_by('-votes').first()
                                if winner:
                                    winners_list.append({
                                        'position': winner.position.name,  # Assuming position has a name field
                                        'contestant': winner.name,
                                        'votes': winner.votes,
                                    })

                        # Update the winners field in the election
                        election_instance.winners = winners_list
                        election_instance.is_ended = True  # Mark the election as ended
                        election_instance.save()

                    else:
                        # If the election is not yet finished, return a message
                        return Response({'message': 'Election is still ongoing. Winners will be calculated after stop time.'}, status=status.HTTP_200_OK)

                except Election.DoesNotExist:
                    # If the election does not exist, return a 404 error
                    return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)

        # Return the original response
        return response

    return _wrapped_view























# # def calculate_winners_decorator(view_func):
# #     def wrapper(self, request, *args, **kwargs):
# #         # Call the view function
# #         response = view_func(self, request, *args, **kwargs)
        
# #         # Get the election associated with the request (adjust the logic if needed)
# #         try:
# #             election = Election.objects.get(id=kwargs['election_id'])  # Adjust this line according to your URL structure
# #             election.calculate_winners()
# #         except Election.DoesNotExist:
# #             return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)

# #         return response
# #     return wrapper








