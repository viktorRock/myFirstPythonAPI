from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, renderers, authentication
from rest_framework.decorators import permission_classes, authentication_classes, detail_route,api_view
from rest_framework.response import Response
from pythapp.permissions import IsOwnerOrReadOnly
from pythapp.serializers import UserSerializer, GroupSerializer, BotSerializer
from pythapp.nltk.nltkutil import NLTKStem, NLTKTokenize, NLTKTag, NLTKner, NLTKLemmatize, NLTKSentiment
from .models import Greeting, Bot

# Tokens
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@permission_classes((permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly))
class BotViewSet(viewsets.ModelViewSet):
    """
     This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        bot = self.get_object()
        return Response(bot.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route(renderer_classes=(renderers.JSONRenderer,))
    def chat(self, request, *args, **kwargs):
        data = request.GET

        #POS tagging
        pos_obj = NLTKTag(data)
        pos_res = pos_obj.pos_tag()
        #NER
        ner_obj = NLTKner(data)
        ner_res = ner_obj.ner()

        #sentiment
        senti_obj = NLTKSentiment(data)
        senti_res = senti_obj.sentiment()

        nltkAux = { 'nltk-NER' : ner_res['result'], 'nltk-POS' : pos_res['result'], 'nletk-Senti' : senti_res['result']}

        res = nltkAux
        return Response(res)

@detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
def index(request):
    return HttpResponse('Hello from Python!')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
