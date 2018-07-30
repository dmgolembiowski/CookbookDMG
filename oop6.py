"""
Property Decorators: Getters, Setters, and Deleters
Allows us to give our class attributes some "Getter" "Setter" and "Deleter"
functionality that's common among other languages
"""
class Employee:
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        # self.email = first + '.' + last + '@email.com'
    
    # def fullname(self):
    #     return '{} {}'.format(self.first, self.last)

    # So we're defining our email in our class like it's a method,
    # but we're able to access it like it's an attribute
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
        # to make a functionality that looks like emp_1.fullname = 'Corey Schafer'
        # would work, we're instead going to have to give it a "setter" so that
        # it overwrites what's already there in the __init__

    # This @fullname.setter must match the @property def's name
    @fullname.setter
    def fullname(self, name):
        # We can just split the parts
        first, last = name.split(' ')
        self.first = first
        self.last = last
    
    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first = None
        self.last = None

emp_1 = Employee('John', 'Smith')

# print('Before we made any silly changes:')
# print(emp_1.first)
# print(emp_1.last)
# print(emp_1.fullname()) --> print(emp_1.fullname)
print('# Now lets overwrite emp_1s first name with:')
emp_1.first = 'Jim'
print('emp_1.first = "Jim"')
print(emp_1.first)
print('# but his email is unfettered: ')
print(emp_1.email)

"""
Since the email didn't automatically update with the 'emp_1.first=Jim' statement
we need a fix that automatically makes the email into 
Jim.Smith@email.com instead of John.Smith@email.com

Using the property decorator:
-Allows us to define a method but we can access it like it's an attribute!
"""
emp_1.fullname = 'Corey Schafer'
print(emp_1.fullname)

"""
You can also make a deleter in the same name. 
Suppose I wanted to delete the fullname of my employee, then
my clean-up code would:

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
        # to make a functionality that looks like emp_1.fullname = 'Corey Schafer'
        # would work, we're instead going to have to give it a "setter" so that
        # it overwrites what's already there in the __init__

    # This @fullname.setter must match the @property def's name
    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first = None
        self.last = None
"""
del emp_1.fullname