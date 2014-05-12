from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('code', 'name')
        model = Country


class VoteHelper(object):
    def __init__(self, vote):
        self.score = vote['score']
        self.country = vote['voting_for__code']


class VoteSerializer(serializers.Serializer):
    """
    """
    score = serializers.IntegerField()
    country = serializers.CharField()
