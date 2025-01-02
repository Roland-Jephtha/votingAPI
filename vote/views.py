from django.shortcuts import render
import random
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.generics import get_object_or_404
from .serializers import UserDataSerializer
from drf_yasg.utils import swagger_auto_schema
import random
import string
# from .mixins import CalculateWinnersMixin
from .decorators import calculate_winners_decorator











class UserDataCreateView(APIView):
    def generate_voters_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))

    @swagger_auto_schema(
        operation_description="Register Users for voting",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='King'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Long'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, example='1234567890'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='ro@gmail.com'),
                'matricnum': openapi.Schema(type=openapi.TYPE_STRING, example='MAT1234567'),
                'department': openapi.Schema(type=openapi.TYPE_STRING, example='Computer Science'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, example='USA'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date', example='1990-01-01'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, example='Male'),
            },
            required=['first_name', 'last_name', 'phone', 'email', 'matricnum', 'department', 'country', 'date_of_birth', 'gender']
        ),
        responses={
            201: openapi.Response(
                description='User Successfully created and voters ID sent via email',
                examples={
                    'application/json': {
                        'message': 'User data saved and voters ID sent via email'
                    }
                }
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            # Generate voters ID
            voters_id = self.generate_voters_id()
            serializer.save(voters_id=voters_id)

            # # Send email to the user
            # email = serializer.validated_data.get('email')
            # subject = "Your Voters ID"
            # email_from = settings.EMAIL_HOST_USER
            # message = f'Hello {serializer.validated_data.get("first_name")}, your voters ID is: {voters_id}'

            # try:
            #     send_mail(subject, message, email_from, [email], fail_silently=False)
            # except Exception as e:
            #     return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'User data saved'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataRetrieveView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve User Details by Voter ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'voters_id': openapi.Schema(type=openapi.TYPE_STRING, example='RVBKN3MZIRX'),
            },
            required=['voters_id']
        ),
        responses={
            200: openapi.Response(
                description='User Details',
                schema=UserDataSerializer,
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        # Retrieve the 'voters_id' from request data
        voters_id = request.data.get('voters_id')
        
        # Validate if 'voters_id' is provided
        if not voters_id:
            return Response({'error': 'voters_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Query the database to find the user by 'voters_id'
        try:
            user_data = User_Data.objects.get(voters_id=voters_id)
        except User_Data.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize and return the user data
        serializer = UserDataSerializer(user_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update User Details by Voter ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'voters_id': openapi.Schema(type=openapi.TYPE_STRING, example='RVBKN3MZIRX'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='King'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Long'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, example='1234567890'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='ro@gmail.com'),
                'matricnum': openapi.Schema(type=openapi.TYPE_STRING, example='MAT1234567'),
                'department': openapi.Schema(type=openapi.TYPE_STRING, example='Computer Science'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, example='USA'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date', example='1990-01-01'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, example='Male'),
            },
            required=['voters_id']  # Voter ID is required for the update
        ),
        responses={
            200: openapi.Response(
                description='User Details Updated Successfully',
                schema=UserDataSerializer,
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
        }
    )
    def patch(self, request, *args, **kwargs):
        # Retrieve the 'voters_id' from request data
        voters_id = request.data.get('voters_id')
        
        # Validate if 'voters_id' is provided
        if not voters_id:
            return Response({'error': 'voters_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Query the database to find the user by 'voters_id'
        try:
            user_data = User_Data.objects.get(voters_id=voters_id)
        except User_Data.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Partially update the user data
        serializer = UserDataSerializer(user_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











class ContestantListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="Register Contestant for Voting",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='King'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Upload contestant image'),
                'position': openapi.Schema(type=openapi.TYPE_STRING, example='1st Position'),
                'tagline': openapi.Schema(type=openapi.TYPE_STRING, example='Bringing innovation to life'),
                'votes': openapi.Schema(type=openapi.TYPE_INTEGER, example=100),
            },
            required=['name', 'image', 'position']  # Required fields
        ),
        responses={
            200: openapi.Response(
                description='List of contestants',
                schema=ContestantSerializer(many=True)
            ),
            201: openapi.Response(
                description='Contestant successfully created with generated contestant ID',
                schema=ContestantSerializer
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    
    def generate_contestant_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))

    def get(self, request):
        contestants = Contestant.objects.all()
        serializer = ContestantSerializer(contestants, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ContestantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            contestant_id = self.generate_contestant_id()
            serializer.save(contestant_id=contestant_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestantDetailView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve, update or delete a contestant",
        responses={
            200: openapi.Response(
                description='Contestant details',
                schema=ContestantSerializer
            ),
            404: openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    }
                }
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    def get_object(self, contestant_id):
        return get_object_or_404(Contestant, id=contestant_id)

    @swagger_auto_schema(
        operation_description="Retrieve a specific contestant",
        responses={
            200: openapi.Response(
                description='Contestant details',
                schema=ContestantSerializer
            ),
            404: openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    }
                }
            )
        }
    )
    def get(self, request, contestant_id):
        contestant = self.get_object(contestant_id)
        serializer = ContestantSerializer(contestant, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific contestant",
        request_body=ContestantSerializer,
        responses={
            200: openapi.Response(
                description='Contestant updated successfully',
                schema=ContestantSerializer
            ),
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            )
        }
    )
    def patch(self, request, contestant_id):
        contestant = self.get_object(contestant_id)
        serializer = ContestantSerializer(contestant, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific contestant",
        responses={
            204: openapi.Response(
                description='Contestant deleted successfully'
            ),
            404: openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    }
                }
            )
        }
    )
    def delete(self, request, contestant_id):
        contestant = self.get_object(contestant_id)
        contestant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Election, Contestant
from .serializers import ElectionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime


class ElectionListCreateView(APIView):
    
    @swagger_auto_schema(
        operation_description="Retrieve all elections or create a new election",
        responses={
            200: openapi.Response(
                description="List of elections",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING, format='time', example='08:00:00'),
                        'stop_time': openapi.Schema(type=openapi.TYPE_STRING, format='time', example='17:00:00'),
                        'no_of_hours': openapi.Schema(type=openapi.TYPE_INTEGER, example=8),
                        'is_ended': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        'contestants': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
                        'winners': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'position': openapi.Schema(type=openapi.TYPE_STRING, example='President'),
                            'contestant': openapi.Schema(type=openapi.TYPE_STRING, example='John Doe'),
                            'votes': openapi.Schema(type=openapi.TYPE_INTEGER, example=150),
                        })
                    })
                )
            ),
            201: openapi.Response(
                description="Election created successfully",
                schema=ElectionSerializer
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    def get(self, request):
        # Retrieve all elections
        elections = Election.objects.all()

        # Calculate winners for elections whose stop_time has passed and not yet ended
        current_time = timezone.now().time()  # Get the current time as a time object
        for election in elections:
            if election.stop_time <= current_time and not election.is_ended:
                # Perform winner calculation for this election
                winners_list = []

                # Group contestants by position
                positions = election.contestants.values_list('position', flat=True).distinct()

                for position in positions:
                    contestants = election.contestants.filter(position=position)

                    if contestants.exists():
                        # Get the contestant with the highest votes for each position
                        winner = contestants.order_by('-votes').first()
                        if winner:
                            winners_list.append({
                                'position': winner.position.name,  # Assuming position has a name field
                                'contestant': winner.name,
                                'votes': winner.votes,
                            })

                # Update the election with the winners and mark it as ended
                election.winners = winners_list
                election.is_ended = True
                election.save()

        # Serialize the elections and return response
        election_serializer = ElectionSerializer(elections, many=True, context={'request': request})
        return Response(election_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new election and determine winners based on contestant votes",
        request_body=ElectionSerializer,
        responses={
            201: openapi.Response(
                description="Election created successfully",
                examples={
                    'application/json': {
                        'message': 'Election created successfully and winners determined',
                        'data': {
                            'id': 1,
                            'start_time': '09:00:00',
                            'stop_time': '18:00:00',
                            'no_of_hours': 9,
                            'is_ended': False,
                            'contestants': [
                                {
                                    'id': 1,
                                    'name': 'John Doe',
                                    'votes': 150,
                                    'position': 'President'
                                },
                                {
                                    'id': 2,
                                    'name': 'Jane Smith',
                                    'votes': 200,
                                    'position': 'Vice President'
                                }
                            ],
                            'winners': [
                                {
                                    'position': 'President',
                                    'contestant': 'John Doe',
                                    'votes': 150
                                },
                                {
                                    'position': 'Vice President',
                                    'contestant': 'Jane Smith',
                                    'votes': 200
                                }
                            ]
                        }
                    }
                }
            ),
            400: openapi.Response(
                description='Bad Request',
                examples={
                    'application/json': {
                        'error': 'Invalid input data'
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        # Validate and create the election
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.save()

            return Response({
                'message': 'Election created successfully',
                'data': ElectionSerializer(election).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














class ElectionDetailView(APIView):
    
    @swagger_auto_schema(
        operation_description="Retrieve, update or delete an election",
        responses={
            200: openapi.Response(
                description="Election details",
                schema=ElectionSerializer
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    # def get_object(self, election_id,):
    #     return get_object_or_404(Election, id=election_id)


    @calculate_winners_decorator
    def get(self, request, election_id):
        elections = Election.objects.get(id = election_id)
        serializer = ElectionSerializer(elections)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update an existing election",
        request_body=ElectionSerializer,
        responses={
            200: openapi.Response(
                description="Election updated successfully",
                schema=ElectionSerializer
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'error': 'Error details'
                    }
                }
            ),
        }
    )
    @calculate_winners_decorator
    def patch(self, request,election_id,):
        election = self.get_object(election_id)
        serializer = ElectionSerializer(election, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py

from .serializers import PositionSerializer


class PositionListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all Positions",
        responses={
            200: PositionSerializer(many=True),
            404: openapi.Response(
                description='No Positions found',
                examples={
                    'application/json': {
                        'error': 'No positions found'
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







class VoterDataListView(APIView):
    """
    GET all User_Data records
    """
    @swagger_auto_schema(
        operation_description="Retrieve a users",
        # request_body=UserDataSerializer

    )
    def get(self, request, *args, **kwargs):
        voters_id = request.query_params.get('voters_id')  # Get the email from query parameters
        if voters_id:
            try:
                user = User_Data.objects.get(voters_id=voters_id)
                serializer = UserDataSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User_Data.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User_Data.objects.all()  # Fetch all users
            serializer = UserDataSerializer(users, many=True)  # Serialize multiple users
            return Response(serializer.data, status=status.HTTP_200_OK)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User_Data, Contestant, UserVote

class UserVoteUpdateAPIView(APIView):


    """
    GET User_Data by voters_id (as a URL parameter)
    """
    @swagger_auto_schema(
        operation_description="Retrieve a user by voters_id",
        # request_body=UserDataSerializer

    )
    def get(self, request, voters_id):
        try:
            # Find the user by voters_id
            user = User_Data.objects.get(voters_id=voters_id)

            # Retrieve all votes associated with this user
            votes = UserVote.objects.filter(user=user)

            # Serialize the votes
            serializer = UserVoteSerializer(votes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User_Data.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        


    """
   PATCH User_Data to update a record by voters_id (as a URL parameter)
    """
    @swagger_auto_schema(
        operation_description="Update User Data by voters_id",
        request_body=UserDataSerializer
    )    


    def patch(self, request, voters_id):
        try:
            user = User_Data.objects.get(voters_id=voters_id)
            voted_data = request.data.get('voted')

            if voted_data:
                for position, contestant_id in voted_data.items():
                    # Find the contestant by ID and filter by position name (case-sensitive)
                    contestant = Contestant.objects.filter(id=contestant_id, position__name=position).first()
                    
                    if contestant:
                        # Add the vote to the contestant and save
                        contestant.votes += 1
                        contestant.save()
                        
                        # Link the contestant to the user's voted field through UserVote model
                        UserVote.objects.create(user=user, contestant=contestant)

                    else:
                        return Response({'error': f'Contestant with ID {contestant_id} for position {position} not found.'}, status=status.HTTP_404_NOT_FOUND)

                return Response({'message': 'Votes updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No vote data provided'}, status=status.HTTP_400_BAD_REQUEST)

        except User_Data.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        










































# class VoterDataRetrieveView(APIView):
#     """
#     GET User_Data by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Retrieve a user by voters_id",
#     )
#     def get(self, request, voters_id, *args, **kwargs):
#         user = get_object_or_404(User_Data, voters_id=voters_id)
#         serializer = UserDataSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class VoterDataPatchView(APIView):
#     """
#     PATCH User_Data to update a record by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Update User Data by voters_id",
#         request_body=UserDataSerializer
#     )
#     def patch(self, request, voters_id, *args, **kwargs):
#         user = get_object_or_404(User_Data, voters_id=voters_id)

#         serializer = UserDataSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# class UserVoteUpdateAPIView(APIView):

#     """
#     GET User_Data by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Retrieve a user by voters_id",
#     )

#     def get(self, request, voters_id):
#         try:
#             user = User_Data.objects.get(voters_id=voters_id)
#             serializer = UserDataSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except User_Data.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
#     """
#     PATCH User_Data to update a record by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Update User Data by voters_id",
#         request_body=UserDataSerializer
#     )

#     def patch(self, request, voters_id):
#         try:
#             user = User_Data.objects.get(voters_id=voters_id)
#             data = request.data.get('voted')
#             if data:
#                 # Update the voted field with new contestant details
#                 user.voted.update(data)
#                 user.save()
#                 return Response({'message': 'Votes updated successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'No vote data provided'}, status=status.HTTP_400_BAD_REQUEST)
#         except User_Data.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)











# class UserVoteUpdateAPIView(APIView):

#     """
#     GET User_Data by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Retrieve a user by voters_id",
#     )
#     def get(self, request, voters_id):
#         try:
#             user = User_Data.objects.get(voters_id=voters_id)
#             serializer = UserDataSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except User_Data.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     """
#     PATCH User_Data to update a record by voters_id (as a URL parameter)
#     """
#     @swagger_auto_schema(
#         operation_description="Update User Data by voters_id",
#         request_body=UserDataSerializer
#     )
#     def patch(self, request, voters_id):
#         try:
#             user = User_Data.objects.get(voters_id=voters_id)
#             data = request.data.get('voted')

#             if data:
#                 # Iterate through voted positions and find corresponding contestants
#                 for position, contestant_name in data.items():
#                     # Find the contestant by name and position
#                     try:
#                         contestant = Contestant.objects.get(id=contestant_name, position__name=position)
#                         # Increment the vote count by 1
#                         contestant.votes += 1
#                         contestant.save()
#                     except Contestant.DoesNotExist:
#                         return Response({'error': f'Contestant {contestant_name} for position {position} not found'}, status=status.HTTP_404_NOT_FOUND)

#                 # Update the user's voted field with new contestant details
#                 user.voted.add(*Contestant.objects.filter(name__in=data.values()))  # Link to Contestant objects
#                 user.save()

#                 return Response({'message': 'Votes updated successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'No vote data provided'}, status=status.HTTP_400_BAD_REQUEST)
#         except User_Data.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

