from django.conf.urls import url, include
from pythapp import views
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'bots', views.BotViewSet)

# router.register(r'digitalparrot',views.index)

# router.register(r'^bots/(?P<pk>[0-9]+)$', views.BotDetail)

# router.register(r'digitalparrot',views.index)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ,url(r'^digitalparrot', views.index, name='index')
    # ,url(r'^bots/$',  views.BotList.as_view())
    # ,url(r'^bots/(?P<pk>[0-9]+)$', views.BotDetail)
]
