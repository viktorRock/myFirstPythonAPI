from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from pythapp.serializers import UserSerializer, GroupSerializer, BotSerializer
from .models import Greeting, Bot
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view,permission_classes,detail_route
from rest_framework.response import Response
from pythapp.permissions import IsOwnerOrReadOnly


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def bot_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        bots = Bot.objects.all()
        serializer = BotSerializer(bots, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        bots = BotSerializer(data=request.data)
        if bots.is_valid():
            bots.save()
            return Response(bots.data, status=status.HTTP_201_CREATED)
        return Response(bots.errors, status=status.HTTP_400_BAD_REQUEST)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def index(request):
    # r = requests.get('http://httpbin.org/status/418')
    # print(r.text)
    return HttpResponse('Hello !' + request.data)
