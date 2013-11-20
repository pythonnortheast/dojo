# countdown.py

import random as r

largePool = [25, 50, 70, 100]



smallPool = range(1,11) * 2

def makeSelection(pool):
    i = r.randint(0, len(pool) - 1)
    return pool.pop(i)

selection = []
selection = [7, 5, 3, 2, 2, 1]

"""
while len(selection) < 6:
    choice = raw_input('Pass in l or s:\n')

    choice = choice.lower()

    if choice == 's':
        selection.append(makeSelection(smallPool))
    elif choice == 'l':
        selection.append(makeSelection(largePool))
"""

print(selection)


def prod(xs):
    return reduce(int.__mul__, xs, 1)

def randSelection():
    selection = []
    
    
    while len(selection) < 6:
        choice = r.choice(['l', 's'])
        choice = choice.lower()

        if choice == 's':
            selection.append(makeSelection(smallPool))
        elif choice == 'l':
            selection.append(makeSelection(largePool))

    return selection

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


# Make list of pairs of factors
def listOfPairs(n):
    s = set([tuple(sorted((x, n/x))) for x in factors(n)])
    return list(s)


def moreFactors(xs):
    return map(factors, xs)
    

##selection = randSelection()


target = r.randint(1, 999)
print 'Target is: ' + str(target)

revList = list(reversed(sorted(selection)))




