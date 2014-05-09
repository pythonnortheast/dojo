from collections import Counter
from random import choice

import requests


CONSONANTS = 'bcdfghjklmnpqrstvwxyz'.upper()
VOWELS = 'aeiou'.upper()

C = 'c'
V = 'v'

def get_consonant():
	"""Gets a random consonant.
	"""
	return choice(CONSONANTS)


def get_vowel():
	"""Gets a random vowel.
	"""
	return choice(VOWELS)

def vowel_or_consonant():
	"""Takes user input and returns whether they want a vowel or a
	consonant.
	"""
	s = raw_input('Would you like a vowel or a consonant?')
	if s == V:
		return get_vowel()
	elif s == C:
		return get_consonant()
	return vowel_or_consonant()


def valid_word(word, chosen_letters):
	"""Returns True or False, if word can be constructed from chosen
	letters.
	"""
	letter_count = Counter(chosen_letters)
	for letter in word.upper():
		if letter not in chosen_letters:
			return False
		if not letter_count[letter]:
			return False
		letter_count[letter] -= 1
	return True


def in_dictionary(word):
	"""Checks an external dictionary and tells us if the word exists.
	"""
	dictionary_url = 'http://services.aonaware.com/DictService/Default.aspx'
	query = {
		'action': 'define',
		'dict': '*',
		'query': word,
	}
	response = requests.get(dictionary_url, params=query)
	return 'No definitions found for ' not in response.text

def get_word():
	"""Gets a word from the user.
	"""
	return raw_input('What word have you found?')

def main():
	letters = tuple(vowel_or_consonant() for i in range(9))
	print letters
	my_word = get_word()
	print valid_word(my_word, letters)
	if valid_word(my_word, letters):
		print in_dictionary(my_word)

main()