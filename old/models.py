
from django.db import models

class SurveyResult(models.Model):
    def __unicode__(self):
        return u'SurveyResult %d' % self.id

class SurveyResultLine(models.Model):
    res = models.ForeignKey(SurveyResult)
    field = models.CharField(max_length=64)
    value = models.IntegerField()

    def __unicode__(self):
        return u'%s: %s=%d' % (self.res, self.field, self.value)
