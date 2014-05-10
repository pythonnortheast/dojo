from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    def total_score(self):
        score = 0
        for c in self.for_country.all():
            score += c.score
        return score

    class Meta:
        ordering = ('name',)

class CountryScore(models.Model):
    for_country = models.ForeignKey(Country, related_name='for_country')
    from_country = models.ForeignKey(Country, related_name='from_country')
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s scored %s from %s' % (self.for_country, self.score, self.from_country)

    class Meta:
        unique_together = (("for_country", "from_country"),)

