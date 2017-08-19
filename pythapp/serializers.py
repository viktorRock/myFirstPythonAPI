from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Bot

class UserSerializer(serializers.HyperlinkedModelSerializer):
    bots = serializers.HyperlinkedRelatedField(queryset=Bot.objects.all(), view_name='bot-detail', many=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'is_staff', 'bots')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class BotSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='bot-highlight', format='html')
    class Meta:
        model = Bot
        fields = ('id', 'name','owner', 'MLmodel', 'created', 'isDeepLearning', 'language', 'style','highlight','linenos')
