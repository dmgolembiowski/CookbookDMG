"""
Input Styles:
"""
"""One approach"""
print('Enter your age: ')
age = input()
age = int(age)


"""An alternative"""
ratio = input('Enter some number with decimal places: ')
ratio = float(ratio)


# List (array/matrix) of data
data = input('Enter the non-uniformly formatted data: ')
"""
Enter the non-umiformly formatted data:
(And you might enter)
Enter the non-umiformly formatted data: asdf fjdk; afed, fjek,asdf, foo
"""
# Bring in regex, a useful data tool  
import re
data = re.split(r'[;,\s]\s*', data)
"""
Line 29 does the following:
  1. "re.split" calls the split method, where r' means raw-string, which helps re.split interpret \s and \s* appropriately
  2. Overwrites "data" with a statement that replaces it with...
     ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
"""


"""Using dictionaries"""
phone_Book = {}
# Add an entry to phone_Book
phone_Book["Paul Erdos"] = '1-800-777-1081'
print(phone_Book["Paul Erdos"])
# '1-800-777-1081'

