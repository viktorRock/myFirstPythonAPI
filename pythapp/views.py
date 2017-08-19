

from django.contrib.auth.models import User, Group
from pythapp.serializers import UserSerializer, GroupSerializer, BotSerializer
from .models import Greeting, Bot
from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, renderers
from rest_framework.decorators import api_view,permission_classes,detail_route
from rest_framework.response import Response
from pythapp.permissions import IsOwnerOrReadOnly
from django.http import HttpResponse

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

class BotViewSet(viewsets.ModelViewSet):
    """
     This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        bot = self.get_object()
        return Response(bot.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

@detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
def index(request):
    # r = requests.get('http://httpbin.org/status/418')
    # print(r.text)
    # return Response('Hello !' + str(request))
    return HttpResponse('Hello from Python!')
