from django.db import models
from datetime import datetime
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Bot(models.Model):
    # today  = datetime.today()
    # defaultName = datetime.today().strftime("%a%d%b%y_%H%M%S")
    # name = models.CharField(max_length=80, blank=True, default=defaultName)
    owner = models.ForeignKey('auth.User', related_name='botrel', on_delete=models.CASCADE)
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default='botty',max_length=80, blank=True, )
    MLmodel = models.TextField()
    isDeepLearning = models.BooleanField(default=False)
    # language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    language = models.CharField(default='python', max_length=100)
    style = models.CharField( default='friendly', max_length=100)


    class Meta:
        ordering = ('created',)
