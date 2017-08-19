from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Bot

class UserSerializer(serializers.HyperlinkedModelSerializer):
    botrel = serializers.PrimaryKeyRelatedField(many=True, queryset=Bot.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'is_staff', 'botrel')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id','created', 'name', 'MLmodel', 'isDeepLearning', 'language', 'style')
        owner = serializers.ReadOnlyField(source='owner.username')
