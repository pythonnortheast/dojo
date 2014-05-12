from django.db import models

class Country(models.Model):
    code = models.SlugField()
    name = models.CharField(max_length=100)


class Vote(models.Model):
    voting_country = models.ForeignKey(Country, related_name='voted_by')
    points = models.IntegerField()
    voting_for = models.ForeignKey(Country, related_name='voted_for')
