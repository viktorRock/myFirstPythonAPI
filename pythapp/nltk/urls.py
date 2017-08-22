from django.conf.urls import url
from pythapp import views
from pythapp.nltk import nltk_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^api/$', nltk_views.HomeView.as_view()),
    url(r'^api/lemma/$', nltk_views.LemmatizeView.as_view()),
    url(r'^api/tag/$', nltk_views.POSTagView.as_view()),
    url(r'^api/ner/$', nltk_views.NERView.as_view()),
    url(r'^api/sentiment/$', nltk_views.SentimentView.as_view()),
]
