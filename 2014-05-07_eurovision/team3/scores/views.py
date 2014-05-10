from django.http import HttpResponse
from django.shortcuts import render
import json

from models import Country, CountryScore

def dumps(request):
    """
        Simple view to return basic json respone of scores
    """
    cs = Country.objects.all().prefetch_related('for_country')
    json_cs = {}

    for c in cs:
        scores = {}
        for s in c.for_country.all():
            scores[s.from_country.name] = s.score
        json_cs[c.name] = {'total_score':c.total_score(),'scores':scores}

    sorted_total_scores = sorted(json_cs.items(),key=lambda x: x[1]['total_score'],reverse=True)

    return HttpResponse(json.dumps(sorted_total_scores), content_type="application/json")
