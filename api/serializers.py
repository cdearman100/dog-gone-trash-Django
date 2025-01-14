from rest_framework import serializers
from .models import TrashLocation, Reward
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'reward_points']

class TrashLocationSerializer(serializers.ModelSerializer):
    users_joined = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = TrashLocation
        fields = ['id', 'name', 'date_of_event', 'description', 'date_reported', 'users_joined']
        
               
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'