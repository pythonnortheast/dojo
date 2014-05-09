
one = ["   ",
       " | ",
       " | "]

two = [" _ ",
       " _|",
       "|_ "]

three = [" _ ",
       " _|",
       " _|"]

four = ["  ",
       "|_|",
       "  |"]

five = ["  _",
       "|_ ",
       " _|"]

six = ["  _",
       "|_ ",
       "|_|"]

seven = ["  _",
       "  |",
       "  |"]

eight = ["  _",
       "|_|",
       "|_|"]

nine = ["  _",
       "|_|",
       "  |"]

zero = [" _ ",
       "| |",
       "|_|"]


numbers = [one, two, three, four, five, six, seven, eight, nine, zero]

lookup = {1: one,
          2: two,
          3: three,
          4: four,
          5: five,
          6: six,
          7: seven,
          8: eight,
          9: nine,
          0: zero}

numbers = range(0,10)

def print_lcd(list_numbers):
    ret_string = ""
    for rownum in range(0,2+1):
        row_str = ""
        for num in list_numbers:
            row_str += lookup[num][rownum]
        print row_str



# for num in numbers:

raw_in = raw_input('in string')
# (map read-string (split " " raw_in))
print_lcd([int(s) for s in raw_in.split() if s.isdigit()])




# loop thru columns:
# for n in range(0,2):
#     row = ""
#     for num in numbers:
#         print len(num)
