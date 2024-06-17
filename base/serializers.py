from rest_framework import serializers
from base.models import Message, CustomUser

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['author', 'replyTo', 'text', 'imageUrl', 'id']
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_staff', 'password'] 

# class PutEventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['start', 'end', 'color', 'name', 'id']

# class UpcomingEventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['start', 'end', 'date', 'color', 'name']

# class SearchEventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'

# # class CustomUserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = CustomUser
# #         fields = ['username', 'is_staff']

# # class CollabSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = CollabMember
# #         fields = '__all__'