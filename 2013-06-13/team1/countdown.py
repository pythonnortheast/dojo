import random
import subprocess
from itertools import permutations
import time

def play_music():
    return subprocess.Popen(['--new-window','http://www.youtube.com/watch?v=5USLUY3c-dk'], 0, 'chrome.exe')

def get_words(filename='words.txt'):
    return frozenset([w.strip() for w in open('words.txt','rb').readlines()])

    
class LettersGame(object):
    words = get_words()
    letters = {
        'v': 'aeiou',
        'c': 'bcdfghjklmnpqrstvwxyz'
    }
    
    def __init__(self):
        self.board = []

    @property
    def board(self):
        return self._board
    
    @board.setter
    def board(self, board):
        self._board = [b.lower() for b in board]
        
    @property
    def permutations(self):
        if not hasattr(self, '_permutations'):
            self._permutations = {}
            for n in range(9):
                n = n+1
                self._permutations[n] = frozenset([''.join(p) for p in permutations(self.board, n)])
        return self._permutations

    @property
    def solutions(self):
        if not hasattr(self, '_solutions'):
            self._solutions = {}
            for n in range(9):
                n = n+1
                self._solutions[n] =  self.permutations[n] & self.words
        return self._solutions

    def choose(self, letter):
        if len(self.board) < 9:
            try:
                self.board.append(random.choice(self.letters[letter.lower()]))
            except KeyError:
                print("Please chose either V or C.")
        else:
            print("You've chosen your board")
        self.display()
            
    def display(self):
        print('{}'.format(''.join([l.upper() for l in self.board])))
    
    def play(self):
        print("Let's get ready to rumble! Choose your letters.")

        while len(self.board) < 9:
            self.choose(raw_input('Vowel or Consonant: '))

        m = play_music()
        time.sleep(35)

        #while raw_input('Solve it [Y]? ').lower() != 'y':
        #    pass
        
        m.terminate()

        for n in range(9, 1, -1):
            s = self.solutions[n]
            if s:
                print('{} letters: {}'.format(n, ', '.join([l.capitalize() for l in s])))


if __name__ == '__main__':
    game = LettersGame()
    game.play()
