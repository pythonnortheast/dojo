import itertools
import collections
import random


def parse_word_list(word_list):
    """Take a list of words and return a dict of words using
    sorted words as keys"""
    word_dict = {}
    for word in word_list:
        sorted_word = ''.join(sorted(list(word)))
        try:
            word_dict[sorted_word].append(word)
        except KeyError:
            word_dict[sorted_word] = [word]
    return word_dict


class Countdown(object):
    words = parse_word_list([line.lower().strip() for line in open('words.txt','rb').readlines()])
    letters = {
        'v': 'aeiou',
        'c': 'bcdfghjklmnpqrstvwxyz'
    }
    
    def __init__(self, board_size=9):
        self.board = []
        self.board_size = board_size
    
    def prepare_word_key(self, word=None):
        if word is None:
            word = self.board
        return ''.join(sorted([w.strip().lower() for w in word if w.strip().lower()]))

    def solutions(self):
        """Return all possible combinations of sorted letters"""
        board_key = self.prepare_word_key()
        solutions = collections.OrderedDict()
        for letter_length in range(len(board_key), 0, -1):
            solutions[letter_length] = []
            for combination in itertools.combinations(board_key, letter_length):
                solutions[letter_length] += self.words.get(self.prepare_word_key(combination),[])
            solutions[letter_length] = sorted(list(set(solutions[letter_length])))
            if not solutions[letter_length]:
                del solutions[letter_length]
        return solutions
    
    def solve(self):
        solutions = self.solutions()
        if solutions:
            print('The solutions to "{}" are...'.format(''.join(self.board).upper()))
            for letter_length,words in solutions.items():
                print('\n{} letters:'.format(letter_length))
                print('{}'.format(', '.join([word.capitalize() for word in words])))

    def choose(self, letter):
        if len(self.board) < self.board_size:
            try:
                self.board.append(random.choice(self.letters[letter.lower()]))
            except KeyError:
                print("Please chose either V or C.")
        self.display()

    def display(self):
        print('{}'.format(''.join([l.upper() for l in self.board])))
    
    def play(self):
        print("Let's get ready to rumble! Choose your letters.")
        while len(self.board) < self.board_size:
            self.choose(raw_input('Vowel or Consonant: '))
        self.solve()


if __name__ == '__main__':
    game = Countdown()
    game.play()
