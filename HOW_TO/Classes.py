#!/usr/bin/env python3
"""Proceed to line ## for a frustrating shortcut"""

# Suppose the following are applicable for a class called Book:
class Novel:
    def __init__(self, Title, Author, ISBN):
        self.Title = Title
        self.Author = Author
        self.ISBN = ISBN
        self.rating = 0
        
    def ny_Times(self, star_Count):
        self.rating = round(float(star_Count), 2)
    
# Now let's see it in action:
LWW = Novel("The Chronicles of Narnia: The Lion, the Witch, and the Wardrobe", "C.S. Lewis", '9780064404990')
SME = Novel("The Shaping of Middle-Earth", "J.R.R. Tolkien", '0345400437')

# What happens when you type in LWW into the python interpreter?
# What about when you type LWW.Title ?

# Next, let's give LWW a rating besides 0 out of 5
LWW.ny_Times(4.682)

# So now, we access that rating with:
print(LWW.rating)

"""
I'll go through the effort of writing out a class
because it's useful for managing data collections,
and maybe performing mathematical operations with
particular class instances.

Maybe in 3061, it'll be particularly useful to multiply 
old ISBN numbers. Here's how you'd do it.
"""

isbn_Product = SME.ISBN * LWW.ISBN
print(isbn_Product)

"""
Okay, this is the part that makes me wonder deeply saddened.
We can also define classes using single one-liners...
"""
from collections import namedtuple
Novel = namedtuple('Novel',['Title', 'Author', 'ISBN', 'rating'])
# That was basically the init method
# Now here's the instantiation with the same objects
LWW = Novel("The Chronicles of Narnia: The Lion, the Witch, and the Wardrobe", "C.S. Lewis", '9780064404990')
SME = Novel("The Shaping of Middle-Earth", "J.R.R. Tolkien", '0345400437')
# Then see what happens when you just type LWW.Author
