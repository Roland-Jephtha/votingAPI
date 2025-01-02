# mixins.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Election

class CalculateWinnersMixin:
    def calculate_winners(self):
        # Get the election associated with the request (adjust the logic if needed)
        try:
            election = Election.objects.get(id=self.kwargs['election_id'])  # Adjust this line according to your URL structure
            election.calculate_winners()
        except Election.DoesNotExist:
            return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)
