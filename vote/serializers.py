from rest_framework import serializers
from .models import *
from django.conf import settings
from rest_framework import serializers
from .models import User_Data, Contestant, Position, UserVote
from datetime import datetime





class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']


class ContestSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)  # Nested serializer for the position field

    class Meta:
        model = Contestant
        fields = ['id', 'name',  'position', 'votes' ]



class UserVoteSerializer(serializers.ModelSerializer):
    contestant = ContestSerializer(read_only=True)  # Nested serializer for Contestant

    class Meta:
        model = UserVote
        fields = ['id', 'contestant', 'voted_at']





class UserDataSerializer(serializers.ModelSerializer):
    voted = UserVoteSerializer(source='uservote_set', many=True, read_only=True)  # Fetch UserVote

    class Meta:
        model = User_Data
        fields = [
            'voters_id', 'first_name', 'last_name', 'phone', 'email', 'matricnum',
            'department', 'country', 'gender', 'voted'
        ]






class ContestantSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)  # Not many=True, since it's a ForeignKey
    
    class Meta:
        model = Contestant
        fields = ['id', 'name', 'image', 'position', 'tagline', 'votes', 'contestant_id']
        read_only_fields = ['id', 'contestant_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if instance.image:
            image_url = instance.image.url
            if request:
                # Adding base URL (domain) to the image URL
                image_url = request.build_absolute_uri(image_url)
            else:
                # Fallback if request is not available in context
                image_url = f'{settings.MEDIA_URL}{instance.image}'
            representation['image'] = image_url

        return representation
    



# Serializer for updating votes in the API
class VoteUpdateSerializer(serializers.Serializer):
    position = serializers.CharField()
    contestant_id = serializers.CharField()

    class Meta:
        fields = ['position', 'contestant_id']



class ElectionSerializer(serializers.ModelSerializer):
    contestants =  serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()  # Not many=True, since it's a ForeignKey
    winners = serializers.JSONField(read_only=True)
    current_server_time = serializers.SerializerMethodField()  # Dynamic time not stored


    class Meta:
        model = Election
        fields = ['id', 'start_time', 'stop_time', 'no_of_hours', 'is_ended', 'contestants', 'winners', 'position', 'current_time', 'current_server_time']

    def get_contestants(self, obj):
        request = self.context.get('request')
        contestants = obj.contestants.all()  # Assuming there is a reverse relation to Contestant model
        return [
            {
                'name': contestant.name,
                'position': contestant.position.name,  # Assuming position is a ForeignKey in the Contestant model
                'votes': contestant.votes,
                'tagline': contestant.tagline,
                'id': contestant.id,
                'image': request.build_absolute_uri(contestant.image.url)
            }
            for contestant in contestants
        ]

    def get_position(self, obj):
        # Customize how contestants are displayed
        position = obj.position.all()  # Assuming there is a reverse relation to Contestant model
        return [
            {
                'name': pos.name,
                
            }
            for pos in position
        ]

    def get_winners(self, obj):
            # Return winners in the desired format
            winners = obj.winners  # Assuming winners are stored in JSON or dict format in the model
            return {
                'president': winners.get('president', ''),
                'vice_president': winners.get('vice_president', ''),
                'sec_general': winners.get('sec_general', ''),
                'sport_director': winners.get('sport_director', ''),
                'financial_secretary': winners.get('financial_secretary', ''),
                'financial_secretary_assistant': winners.get('financial_secretary_assistant', ''),
                'social_director': winners.get('social_director', ''),
                'welfarer': winners.get('welfarer', ''),
                'welfarer_assistant': winners.get('welfarer_assistant', ''),
                'secretary_general': winners.get('secretary_general', ''),
                'treasurer': winners.get('treasurer', '')
            }
    
    # def get_current_time(self, obj):
    #     # Return the current server time
    #     return datetime.now().strftime("%H:%M:%S")



    def get_current_server_time(self, obj):
        # Return the current server time dynamically when the API is called
        return datetime.now().time()  # Return time formatted as a string






















































































































# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = ['name']





# class VotedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contestant
#         fields = ['id',  'position']




# class ContestantSerializer(serializers.ModelSerializer):
#     position = PositionSerializer(read_only=True)  # Not many=True, since it's a ForeignKey
    
#     class Meta:
#         model = Contestant
#         fields = ['id', 'name', 'image', 'position', 'tagline', 'votes', 'contestant_id']
#         read_only_fields = ['id', 'contestant_id']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         request = self.context.get('request')

#         if instance.image:
#             image_url = instance.image.url
#             if request:
#                 # Adding base URL (domain) to the image URL
#                 image_url = request.build_absolute_uri(image_url)
#             else:
#                 # Fallback if request is not available in context
#                 image_url = f'{settings.MEDIA_URL}{instance.image}'
#             representation['image'] = image_url

#         return representation
    



# class ContestSerializer(serializers.ModelSerializer):
#     position = PositionSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Contestant
#         fields = ['name', 'position' ]



# class VoteSerializer(serializers.Serializer):
#     president = serializers.CharField(allow_blank=True, required=False)
#     vice_president = serializers.CharField(allow_blank=True, required=False)
#     sec_general = serializers.CharField(allow_blank=True, required=False)
#     sport_director = serializers.CharField(allow_blank=True, required=False)
#     financial_secretary = serializers.CharField(allow_blank=True, required=False)
#     financial_secretary_assistant = serializers.CharField(allow_blank=True, required=False)
#     social_director = serializers.CharField(allow_blank=True, required=False)
#     welfarer = serializers.CharField(allow_blank=True, required=False)
#     welfarer_assistant = serializers.CharField(allow_blank=True, required=False)

# class UserDataSerializer(serializers.ModelSerializer):
#     voted = VoteSerializer()

#     class Meta:
#         model = User_Data
#         fields = ['voters_id', 'first_name', 'last_name', 'phone', 'email', 'matricnum', 'department', 'country', 'date_of_birth', 'gender', 'voted']







# # class UserDataSerializer(serializers.ModelSerializer):
# #     voted = VotedSerializer(many=True, read_only=True)  # Nested representation for voted

# #     class Meta:
# #         model = User_Data
# #         fields = '__all__'  # Include all fields from User_Data






# class ElectionSerializer(serializers.ModelSerializer):


# class VoterDataSerializer(serializers.ModelSerializer):
#     voted = VotedSerializer(many=True, read_only=True)  # Nested representation for voted field

#     class Meta:
#         model = User_Data
#         fields = '__all__'









