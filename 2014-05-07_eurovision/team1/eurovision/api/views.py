import json

from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import Country, Vote
from .rest import CountrySerializer, VoteHelper, VoteSerializer


class CountryView(ListAPIView):
    model = Country
    serializer_class = CountrySerializer


class VoteView(ListCreateAPIView):
    lookup_field = 'voting_country'
    model = Vote

    def get_queryset(self):
        """
        """
        return Vote.objects.filter(
            voting_country__code=self.kwargs[self.lookup_field])

    def create(self, request, *args, **kwargs):
        """Take each country's vote set and translate it to points for each
        country
        """
        data = json.loads(request.stream.read())
        vote_allocation = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
        voting_country = Country.objects.get(
            code=self.kwargs[self.lookup_field])

        for country, points in zip(data, vote_allocation):
            vote = Vote.objects.create(
                voting_country=voting_country,
                points=points,
                voting_for=Country.objects.get(code=country))
        return HttpResponse()


class ScoreView(ListAPIView):
    model = Vote
    serializer_class = VoteSerializer

    def get_queryset(self):
        """
        """
        voting_for = Vote.objects.values('voting_for__code').annotate(
            score=Sum('points')).order_by('score')

        rtn = []

        for vote in voting_for:
            rtn.append(VoteHelper(vote))
        return rtn
