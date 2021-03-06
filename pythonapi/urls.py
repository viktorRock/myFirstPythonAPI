"""tutorial URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
1. Add an import:  from my_app import views
2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
1. Add an import:  from other_app.views import Home
2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
1. Import the include() function: from django.conf.urls import url, include
2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from pythapp import views,myauth
from pythapp.nltk import nltk_views, urls
from rest_framework import routers, serializers, viewsets, authtoken
from django.contrib import admin
from pythapp.myauth import urls

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'bots', views.BotViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(myauth.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^digitalparrot', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/$', nltk_views.HomeView.as_view()),
    url(r'^api/lemma/$', nltk_views.LemmatizeView.as_view()),
    url(r'^api/tag/$', nltk_views.POSTagView.as_view()),
    url(r'^api/ner/$', nltk_views.NERView.as_view()),
    url(r'^api/sentiment/$', nltk_views.SentimentView.as_view()),
    url(r'^api-token-auth/', authtoken.views.obtain_auth_token),
]
# urlpatterns += format_suffix_patterns(urlpatterns)
