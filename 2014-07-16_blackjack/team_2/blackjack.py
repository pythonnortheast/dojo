"""
Blackjack implementation

Some bugs but essentially a working implementation
"""

import random
deck = [ ]

for suit in range(4):
    for number in range(13):
        deck.append((suit, number))

random.shuffle(deck)

def card_repr(card):
    suits = "hearts", "spades", "diamonds", "clubs"
    cards = "ace", "deuce", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"
    return "\t%s of %s" %(cards[card[1]], suits[card[0]])

def deal(deck_instance, hand, num = 1):
    for i in range(num):
        hand.append(deck_instance.pop())

def print_hand(hand):
    for card in hand:
        print(card_repr(card))

    print("\t(%d)" % best_value(hand))

def best_value(hand):
    card_value = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    value = sum(card_value[c[1]] for c in hand)
    sorted_hand = list(reversed(sorted((card_value[c[1]] for c in hand))))

    while value > 21 and sorted_hand[0] == 11:
        value -= 10
        sorted_hand.pop()
    return value


def check_twentyone(hand):
    return best_value(hand) == 21


def is_bust(hand):
    return best_value(hand) > 21


def compare_hand(hand1, hand2):
    """
    Return True if first hand better than second
    (in case of same value, hand1 always wins)
    """

    for hand in (hand1, hand2):
        assert(not is_bust(hand))

    return best_value(hand1) >= best_value(hand2)

def game_loop():
    print("\nSTART OF GAME\n")
    player_hand = []
    dealer_hand = []
    deal(deck, player_hand, 2)

    deal(deck, dealer_hand, 2)

    while True:
        print("------")
        print("Player hand:")

        print_hand(player_hand)
        print("\n")

        print("Dealer hand:")
        print_hand(dealer_hand)
        print("\n")


        if check_twentyone(player_hand):
            if check_twentyone(dealer_hand):
                print("Dealer wins")
            else:
                print("player wins")
            break

        if is_bust(player_hand):
            print("You went bust!")
            break

        if is_bust(dealer_hand):
            print("Dealer went bust!")
            break

        answer = None

        if best_value(player_hand) >= 16:
            while answer not in ('Y', 'N'):
                answer = input("Another Card? [Y/N]: ").upper()

        if answer == 'N':
            while best_value(dealer_hand) < best_value(player_hand):
                deal(deck, dealer_hand, 1)

            dealer_won = not is_bust(dealer_hand) and compare_hand(dealer_hand, player_hand)

            print("Final hands: \n" )

            print_hand(player_hand)
            print("\n")

            print("Dealer hand:")
            print_hand(dealer_hand)
            print("\n")
            if dealer_won:
                print("Dealer won")
            else:
                print("You won")

            break
        else:
            deal(deck, player_hand, 1)
            deal(deck, dealer_hand, 1)



if __name__ == '__main__':
    print("*** Welcome to Campus North Casino ***\n")
    while True:
        game_loop()
