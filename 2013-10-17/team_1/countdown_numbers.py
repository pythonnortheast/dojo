import random
target = random.randint(0, 999)
print 'Your target is ', target
big_numbers = [25, 50, 75, 100]
small_numbers = range(1, 11) * 2
num_big_nums = input('How many big numbers would you like?')
num_small_nums = 6 - num_big_nums
random.shuffle(big_numbers)
random.shuffle(small_numbers)
chosen_big_numbers = big_numbers[: num_big_nums]
print chosen_big_numbers
chosen_small_numbers = small_numbers[: num_small_nums]
print chosen_small_numbers

current_closest = (0, '')

while current_closest[0] != target:
    numbers = [(n, str(n)) for n in chosen_small_numbers + chosen_big_numbers]

    while len(numbers) > 1:
        new_num = (-1, '')
        random.shuffle(numbers)
        operator = random.randint(0, 3)
        no_1 = numbers.pop(0)
        no_2 = numbers.pop(0)
        if operator == 0:
            new_num = (no_1[0] + no_2[0], '(%s+%s)' % (no_1[1], no_2[1]))
        elif operator == 1:
            if no_1[0] > no_2[0]:
                new_num = (no_1[0] - no_2[0], '(%s-%s)' % (no_1[1], no_2[1]))
            else:
                new_num = (no_2[0] - no_1[0], '(%s-%s)' % (no_2[1], no_1[1]))
        elif operator == 2:
            new_num = (no_1[0] * no_2[0], '%s*%s' % (no_1[1], no_2[1]))
        else:
            if no_1[0] > no_2[0]:
                if no_2[0] == 0 or no_1[0] % no_2[0] != 0:
                    numbers.append(no_1)
                    numbers.append(no_2)
                else:
                    new_num = (no_1[0] / no_2[0], '%s/%s' % (no_1[1], no_2[1]))
            else:
                if no_1[0] == 0 or no_2[0] % no_1[0] != 0:
                    numbers.append(no_1)
                    numbers.append(no_2)
                else:
                    new_num = (no_2[0] / no_1[0], '%s/%s' % (no_2[1], no_1[1]))

        if new_num[0] > 0:
            numbers.append(new_num)

        if new_num[0] > 0 and abs(new_num[0] - target) <\
            abs(current_closest[0] - target):
            current_closest = new_num
            print current_closest

    if len(numbers) >0 and abs(numbers[0][0] - target) <\
            abs(current_closest[0] - target):
            current_closest = numbers[0]
            print current_closest





