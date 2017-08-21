import os.path
from pickle import load, dump

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize, pos_tag, UnigramTagger, BigramTagger, RegexpTagger, ne_chunk, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import brown
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from .nltk_constants import DEFAULT_STEMMER, DEFAULT_TOKENIZER, DEFAULT_TAGGER, DEFAULT_TRAIN, TRAINERS



class NLTKStem(object):
    """
    NLTK Stemmers used: Porter, Snowball and Lancaster

    Accepts:

    /api/stem?words=<words>/
    /api/stem?words=<words>&stemmer=<porter/snowball/lancaster/default>/
    /api/stem?words=<words>&stemmer=snowball&language=<language>&ignore_stopwords=<true/false>/

    Query Parameters:

        * Mandatory:
            1. words:
                type: string comma separated
        * Optional:
            1. stemmer:
                value: porter/snowball/lancaster/default
                default: snowball
            2. ignore_stopwords: Only for Snowball Stemmer
                value: true/false
                default: false
            3. language: Only for Snowball Stemmer
                value: see SnowballStemmer.languages
                default: english
    """

    dispatch = {
        'porter': PorterStemmer,
        'snowball': SnowballStemmer,
        'lancaster': LancasterStemmer,
    }
    dispatch['default'] = dispatch[DEFAULT_STEMMER]

    def __init__(self, options):
        self.options = options

    def stem(self):
        words = self._clean(self.options['words'])
        stemmer = self.options.get('stemmer', DEFAULT_STEMMER)
        stemmer_obj = self.dispatch.get(stemmer, self.dispatch[DEFAULT_STEMMER])
        result = []

        if stemmer_obj == SnowballStemmer:
            ignore_stopwords = False

            if self.options.get('ignore_stopwords'):
                if self.options['ignore_stopwords'] == 'true':
                    ignore_stopwords = True
            language = self.options.get('language', 'english')

            result = [stemmer_obj(language, ignore_stopwords).stem(word)
                      for word in words]
        else:
            result = [stemmer_obj().stem(word) for word in words]

        return self._dump(result)

    def _clean(self, words):
        return words.split(',')

    def _dump(self, result):
        response = {
            'status': True,
            'result': result
        }
        return response


class NLTKTokenize(object):
    """
    NLTK Tokenizers used: word_tokenize, StringTokenizer, TweetTokenizer

    Accepts:

    /api/tokenize?sentence=<sentence>/
    /api/tokenize?sentence=<sentence>&tokenizer=<word/tweet/default>/

    Query Parameters:

        * Mandatory:
            1. sentence:
                type: string
        * Optional:
            1. tokenizer:
                value: word/tweet/default
                default: word_tokenize
    """

    dispatch = {
        'word': word_tokenize,
        'tweet': TweetTokenizer,
    }
    dispatch['default'] = dispatch[DEFAULT_TOKENIZER]

    def __init__(self, options):
        self.options = options

    def tokenize(self):
        tokenizer = self.options.get('tokenizer', DEFAULT_TOKENIZER)
        tokenizer_obj = self.dispatch.get(tokenizer,
                                          self.dispatch[DEFAULT_TOKENIZER])

        if tokenizer_obj == word_tokenize:
            result = tokenizer_obj(self.options['sentence'])

        else:
            result = tokenizer_obj().tokenize(self.options['sentence'])

        return self._dump(result)

    def _dump(self, result):
        response = {
            'status': True,
            'result': result
        }
        return response


class NLTKTag(object):
    """
    NLTK POS tagger used: pos_tag, UnigramTagger, BigramTagger & RegexpTagger

    Accepts:

    /api/tag?sentence=<sentence>/
    /api/tag?sentence=<sentence>&tagger=<pos/unigram/bigram/default>/
    /api/tag?sentence=<sentence>&tagger=<pos/unigram/bigram/default>&train=<categories>/
    including any query parameter accepted by /api/tag/

    Query Parameters:

        * Mandatory:
            1. sentence:
                type: string

        * Optional:
            1. tagger:
                value: pos/unigram/bigram/regex
                default: pos_tag
            2. train (iff unigram/bigram):
                value: 'news', 'editorial', 'reviews', 'religion',
                       'learned', 'science_fiction', 'romance', 'humor'
                default: 'news'
            3. any query parameter acceptable by /api/tag/
    """

    def __init__(self, options):
        self.options = options

    def pos_tag(self):
        tokenize_obj = NLTKTokenize(self.options)
        res = tokenize_obj.tokenize()
        tokens = res['result']
        tags = []

        # Performs Bigram / Unigram / Regex Tagging
        if self.options.get('tagger') in ['unigram', 'bigram', 'regex']:
            trainer = self.options['train'] if self.options.get(
                'train') in TRAINERS else DEFAULT_TRAIN

            train = brown.tagged_sents(categories=trainer)

            # Create your custom regex tagging pattern here
            regex_tag = RegexpTagger([
                (r'^[-\:]?[0-9]+(.[0-9]+)?$', 'CD'),
                (r'.*able$', 'JJ'),
                (r'^[A-Z].*$', 'NNP'),
                (r'.*ly$', 'RB'),
                (r'.*s$', 'NNS'),
                (r'.*ing$', 'VBG'),
                (r'.*ed$', 'VBD'),
                (r'.*', 'NN')
            ])

            current = os.path.dirname(os.path.abspath(__file__))

            # Unigram tag training data load / dump pickle
            pkl_name = current + '/trained/unigram_' + trainer + '.pkl'
            if os.path.isfile(pkl_name):
                with open(pkl_name, 'rb') as pkl:
                    unigram_tag = load(pkl)
            else:
                unigram_tag = UnigramTagger(train, backoff=regex_tag)
                with open(pkl_name, 'wb') as pkl:
                    dump(unigram_tag, pkl, -1)

            # Bigram tag training data load / dump pickle
            if self.options['tagger'] == 'bigram':
                pkl_name = current + '/trained/bigram_' + trainer + '.pkl'
                if os.path.isfile(pkl_name):
                    with open(pkl_name, 'rb') as pkl:
                        bigram_tag = load(pkl)
                else:
                    bigram_tag = BigramTagger(train, backoff=unigram_tag)
                    with open(pkl_name, 'wb') as pkl:
                        dump(bigram_tag, pkl, -1)
                tags = bigram_tag.tag(tokens)  # Bigram tagging performed here
            elif self.options['tagger'] == 'unigram':
                tags = unigram_tag.tag(tokens)  # Unigram tagging performed here
            else:
                tags = regex_tag.tag(tokens)  # Regex tagging performed here

        # Performs default pos_tag
        elif self.options.get('tagger', DEFAULT_TAGGER) == 'pos':
            tags = pos_tag(tokens)

        return self._dump(tags)

    @staticmethod
    def _dump(result):
        response = {
            'status': True,
            'result': result
        }
        return response


class NLTKner(object):
    """
    NLTK NER used: ne_chunk

    Accepts:

    /api/ner?sentence=<sentence>/
    including any query parameter accepted by /api/tag/

    Query Parameters:

        * Mandatory:
            1. sentence:
                type: string

        * Optional:
            1. any query parameter acceptable by /api/tag/
    """

    def __init__(self, options):
        self.options = options

    def ner(self):
        pos_obj = NLTKTag(self.options)
        res = pos_obj.pos_tag()

        tagged_sentence = res['result']
        chunked_sentence = ne_chunk(tagged_sentence)
        tokens = self._parse(chunked_sentence)
        return self._dump(tokens)

    def _parse(self, tree):
        n_tokens = []
        for node in tree:
            if isinstance(node, nltk.tree.Tree):
                if node.label() in ['NE', 'PERSON']:
                    for leaf in node.leaves():
                        n_tokens.append(leaf[0])
        return n_tokens

    def _dump(self, tokens):
        response = {
                'status': True,
                'result': tokens
                }
        return response


class NLTKLemmatize(object):
    """
    NLTK Lemmatizer used: WordNetLemmatizer

    Accepts:
    /api/lemma?words=<words>/

    Query Parameters:

        * Mandatory:
            1. words:
                type: string comma separated
    """

    def __init__(self, options):
        self.options = options

    def lemma(self):
        lemma_obj = WordNetLemmatizer()
        words = self._clean(self.options['words'])
        result = [lemma_obj.lemmatize(word) for word in words]
        return self._dump(result)

    def _clean(self, words):
        return words.split(',')

    def _dump(self, result):
        response = {
                'status': True,
                'result': result
                }
        return response


class NLTKSentiment(object):
    """
    NLTK Sentiment Analyzer used: vader

    Accepts:
    /api/sentiment?sentence=<sentence>/

    Query Parameters:

        * Mandatory:
            1. sentence:
                type: string
    """

    def __init__(self, options):
        self.options = options

    def sentiment(self):
        sentiment_obj = SentimentIntensityAnalyzer()
        result = sentiment_obj.polarity_scores(self.options['sentence'])
        return self._dump(result)

    def _dump(self, result):
        response = {
                'status': True,
                'result': result
                }
        return response
