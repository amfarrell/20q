from django.db import models
import dummy

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

#    def __init__(self):
#        underlying = dummy.StatefulGame()
#    def state(self):
#        return self.underlying.state

