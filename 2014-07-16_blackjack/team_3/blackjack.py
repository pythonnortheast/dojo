#!/usr/bin/env python
# coding: utf-8
"""
Blackjack game - dojo version. Choosing low value for ace card
works only for the player (not the dealer).

"""
import random

DECKS = 1


def draw(cards):
	"""
	Draw a random card from a set of cards.

	""""
	f = lambda x: cards[x] > 0
	card = random.choice(filter(f, keys))
	cards[card] -= 1
	return card


def dealer(cards, player_score):
	"""
	Play as dealer. Draw cards until the player's score is beaten.

	"""
	hand = [draw(cards), draw(cards)]
	dealer_score = find_score(hand)

	while dealer_score < player_score:
		hand.append(draw(cards))
		dealer_score = find_score(hand)

	return hand, dealer_score


def find_score(hand):
	"""
	Returns a score for a given hand.

	"""
	score = 0
	for card in hand:
		try:
			score += int(card)
		except ValueError:
			if card == "A":
				score += 11
			else:
				score += 10
	return score


def play(cards):
	"""
	Play one round of the game with given cards.

	"""
	low = 0

	hand = [draw(cards), draw(cards)]
	print hand

	while True:
		choice = raw_input("(pass, low, <enter>? ")

		if choice == 'pass':
			player_score = find_score(hand) - low
			dealer_hand, dealer_score = dealer(cards, player_score)
			print "My hand is", dealer_hand

			if player_score == dealer_score:
				print "Draw, ahhh!"
			elif 21 >= dealer_score > player_score:
				print "Dealer wins Nah Nah Nah Nah Nah Nah"
			else:
				print "You win, eat my shorts"
			break
		else:
			# if player decides to use low value for an ace, remeber it
			if choice == "low":
				if hand[-1] == "A" or hand[0] == "A" and len(hand) < 3:
					low += 10

			hand.append(draw(cards))
			print hand

			if find_score(hand) - low > 21:
				print "Ha Ha you loose!!"
				break


# setup the cards using DECKS many decks
keys = [str(i) for i in range(2,11)] + 'J Q K A'.split()
cards = {key:DECKS * 4 for key in keys}

print "Hello let's play"

while True:
	play(cards)
	if raw_input("again (y/n)? ") is not "y":
		print "Goodbye, we will meet again"
		break
