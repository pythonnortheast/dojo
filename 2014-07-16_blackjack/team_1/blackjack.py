import random

ACE_CARD = 0

class Player(object):
	def __init__(self, is_dealer=False):
		"""Construct the Player instance 
		"""
		self.total = 0
		self.is_dealer = is_dealer

	def draw(self, decks):
		"""Pick a card from the decks
		"""
		self.total += self.get_value(decks.pop())
		self.check_value()

	def start(self, decks):
		"""Draw two cards at start
		"""
		self.draw(decks)
		self.draw(decks)

	def check_value(self):
		name = 'Dealer' if self.is_dealer else 'Player'
		print '{} value: {}'.format(name, self.total)

	def get_value(self, card):
		"""Determine card value
		"""
		value = card

		if value == ACE_CARD:
			if self.is_dealer:
				value = 11 if self.total + 11 <= 21 else 1
			else:
				choice = ''
				while choice.lower() not in ('h', 'l'):
					choice = raw_input('ACE: High or Low?')
					if choice == 'H':
						value = 11
						break
					elif choice == 'L':
						value = 1
						break

		return value

def make_decks():
    suit = range(11)
    decks = suit*24
    random.shuffle(decks)
    return decks

def main():
    decks = make_decks()
    hand_number = 0

    player = Player()
    dealer = Player(is_dealer=True)

    player.start(decks)
    dealer.start(decks)

    hand_number += 1

    while hand_number < 4:
    	player.draw(decks)
    	dealer.draw(decks)

if __name__ == '__main__':
    main()