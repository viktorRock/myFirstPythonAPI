from rest_framework import  permissions, authentication
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from pythapp.nltk.nltkutil import NLTKStem, NLTKTokenize, NLTKTag, NLTKner, NLTKLemmatize, NLTKSentiment
from pythapp.permissions import IsOwnerOrReadOnly

# @permission_classes((permissions.IsAdminUser,))
# @authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
# @authentication_classes((authentication.TokenAuthentication,))
# @permission_classes((permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly))
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
class LemmatizeView(APIView):
    """
    View for Lemmatization
    """
    # @api_view(['GET'])
    def get(self, request):
        data = request.GET
        lemma_obj = NLTKLemmatize(data)
        res = lemma_obj.lemma()
        return Response(res)

@permission_classes((permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly))
@authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
class HomeView(APIView):
    """
    Landing Page View
    """
    def get(self, request):
        res = {
            'examples': [
                '/api/stem?words=<word1,word2,word3>',
                '/api/stem?words=<word1,word2>&stemmer=<porter/snowball/lancaster/default>',
                '/api/stem?words=<word1,word2>&stemmer=snowball&language<language>&ignore_stopwords=<true/false>',
                '/api/tokenize?sentence=<sentence>',
                '/api/tokenize?sentence=<sentence>&tokenizer=<word/tweet/default>',
                '/api/tag?sentence=<sentence>',
                '/api/tag?sentence=<sentence>&tagger=<pos/unigram/bigram>',
                '/api/tag?sentence=<sentence>&tagger=<pos/unigram/bigram>&train=<categories>',
                '/api/tag?sentence=<sentence>&tokenizer=<word/tweet/default>',
                '/api/ner?sentence=<sentence>',
                '/api/ner?sentence=<sentence>&tokenizer=<word/tweet/default>',
                '/api/sentiment?sentence=<sentence>'
            ],
            'message': 'see app/util.py for details',
            'repository': 'https://github.com/vipul-sharma20/nltk-api-server',
        }
        return Response(res)

@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
class POSTagView(APIView):
    """
    View for Part Of Speech tagging
    """
    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        data = request.GET
        pos_obj = NLTKTag(data)
        res = pos_obj.pos_tag()

        return Response(res)

@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
class NERView(APIView):
    """
    View for Named Entity Recognition
    """
    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        data = request.GET
        ner_obj = NLTKner(data)
        res = ner_obj.ner()

        return Response(res)

@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication,authentication.SessionAuthentication,))
class SentimentView(APIView):
    """
    View for Sentiment Analysis
    """
    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        data = request.GET
        senti_obj = NLTKSentiment(data)
        res = senti_obj.sentiment()

        return Response(res)
