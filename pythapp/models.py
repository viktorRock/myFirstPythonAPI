from django.db import models
from datetime import datetime
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Bot(models.Model):
    # name = models.CharField(max_length=80, blank=True, default=defaultName)
    owner = models.ForeignKey('auth.User', related_name='bots', on_delete=models.CASCADE)
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=80, blank=True )
    MLmodel = models.TextField()
    isDeepLearning = models.BooleanField(default=False)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,default='friendly',max_length=100)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        today  = datetime.today()
        defaultName = datetime.today().strftime("%a%b%d%y_%H%M%S")

        self.name = self.name or defaultName
        linenos = self.linenos and 'table' or False
        lexer = get_lexer_by_name(self.language)
        options = self.name and {'name': self.name} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.name, lexer, formatter)
        super(Bot, self).save(*args, **kwargs)

        # limit the number of instances retained
        bots = Bot.objects.all()
        if len(bots) > 10:
            bots[0].delete()
