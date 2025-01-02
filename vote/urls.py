from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserDataCreateView.as_view(), name='create-user'),
    path('login/', UserDataRetrieveView.as_view(), name='user-data-retrieve'),
     path('contestants/', ContestantListCreateView.as_view(), name='contestant-list-create'),
    path('contestants/<int:contestant_id>/', ContestantDetailView.as_view(), name='contestant-detail'),
    path('election/', ElectionListCreateView.as_view(), name='election-list-create'),
    path('election/<str:election_id>/', ElectionDetailView.as_view(), name='election-detail'),

    path('voters/', VoterDataListView.as_view(), name='voter-list'),  # Get all User_Data
    # path('voter/<str:voters_id>/', VoterDataRetrieveView.as_view(), name='voter-retrieve'),  # Get by voters_id
    # path('voter/<str:voters_id>/patch/', VoterDataPatchView.as_view(), name='voter-patch'),  # Patch by voters_id

    path('vote/<str:voters_id>/vote/', UserVoteUpdateAPIView.as_view(), name='user-vote-update'),
    path('position/', PositionListView.as_view(), name='position-list-view'),


]






