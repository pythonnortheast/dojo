#!/usr/bin/env python
# coding: utf-8
"""
Each run of this program simulates a round of voting in the Eurovision contest.
To simulate entire competition, run it with the following bash script:
for i in `seq 1 26`; do ./eurovision.py; done

"""
import os
import json
import random

from collections import defaultdict

DATA_FILE = "votes.json"
POINTS = range(1,9) + [10,12]

COUNTRIES = ["Ukraine", "Belarus", "Azerbaijan", "Iceland", "Norway", "Romania",
	"Armenia", "Montenegro", "Poland", "Greece", "Austria", "Germany", "Sweden",
	"France", "Russia", "Italy", "Slovenia", "Finland", "Spain", "Switzerland",
	"Hungary", "Malta", "Denmark", "Netherlands", "San Marino", "United Kingdom"]


# create dictionary using 0 as a default value for new keys
votes = defaultdict(int)

# read the previous votes if exist
if os.path.exists(DATA_FILE):
	with open(DATA_FILE) as data:
		votes.update(json.load(data))

# select a random sample of 10 countries
selection = random.sample(COUNTRIES, 10)
# assign points to each country from a sample
new_vote = {country:points for country, points in zip(selection, POINTS)}

# update the votes
for country, points in new_vote.items():
	votes[country] += points

# save votes to a file
with open(DATA_FILE, "wt") as data:
	json.dump(votes, data, sort_keys=True)

# show the top 5 countries (sorted by points)
for country, points in sorted(votes.items(), key=lambda x: -x[1])[:5]:
	print points, country
