"""
Special Methods: Use within classes to emulate builtin behavior within python
and implement operator overload
"""
class Employee:

    raiseAmount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'
        self.pay = pay
    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def applyRaise(self):
        self.pay = int(self.pay * self.raiseAmount)
    """
    __repr__ is meant to be an unambiguous representation of the object 'self'
    it should be used for debugging and logging and things like that
    it's really meant to be seen by other developers!
    if --str-- is used without --repr--, then --str-- will just use --repr-- as a fallback.
    """
    def __repr__(self):
        return "Employee('{}', '{}', {})".format(self.first, self.last, self.pay)
    """
    __str__ is meant to be a readable object and is meant to be used as a display to the end-user
    """
    def __str__(self):
        return '{} - {}'.format(self.fullname(), self.email)

    def __add__(self, other):
        return self.pay + other.pay
    
    def __len__(self):
        return len(self.fullname())
        # We just changed how __len__ behaves by making it print the length of an employee's full name

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'Employee', 60000)

# It would be nice to change the functionality for:
# print(emp_1)
# so that it describes more than 'python object at <0x0000>'
"""
to do this, we have to define a special method (lines 26 - 32)
Special methods, like __init__, are surrounded by 'dunders' or double-underscores
"""
"""
print(emp_1.__repr__())
# Employee('Corey', 'Schafer', 50000)
print(emp_1.__str__())
# Corey Schafer - Corey.Schafer@email.com
"""
"""
adding numbers together actually accesses special methods!
"""
print('These two things are actually the same:')
print('print(1+2)')
print(1+2)
print('print(int.__add__(1,2))')
print(int.__add__(1,2))
# What's actually happening when you do: print(a + b) is actually
# print(str.__add__('a' + 'b')) to CONCATENATE them

"""
Now let's pretend that we needed to come up with a special method that adds two employee instances together
and have the result be their combined salaries, then... have to create "def __add__" method
"""
a = emp_1 + emp_2
print('print(emp_1 + emp_2) = ' + str(a))
print(emp_1 + emp_2)

print('The same sort of thing happens to the len() function which prints out a string length value')
print('The above line has ' + str(len('print("The same sort of thing happens to the len() function which prints out a string length value")')) + ' characters,')
print('which gets accessed by the "print(x.__len__())" special method.')

# Line 37-39
print(len(emp_1))