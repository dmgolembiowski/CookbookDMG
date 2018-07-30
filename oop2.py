# Title
class Employee:

    numOfEmployees = 0
    raiseAmt = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = f'{self.first} + "." + {self.last} + "@company.com"' # Ignore the dangerous syntax error
        self.pay = pay

        Employee.numOfEmployees += 1
    
    def fullName(self):
        return '{} {}'.format(self.first, self.last)

    def applyRaise(self):
        self.pay = int(self.pay * self.raiseAmt)

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raiseAmt = amount

    # Create a class constructor to make adding new instances from strings easier
    @classmethod
    def from_str(cls, emp_str):
        first, last, pay = emp_str.split('-')
        # The important part to see is that "Employee(first, last, pay" gets replace with the line below when inserted into the classmethod
        # cls(first, last, pay) # But this just makes it; we need to actually return it for when the method is called
        return cls(first, last, pay)

    # Lastly, static methods are included because they have some logical reason for applying,
    # Yet, they don't need any arguments to be passed
    @staticmethod
    def is_workday(day):
        # The purpose of this method is to be passed (maybe a string like Tuesday) and return True or False if 
        # it applies to the argument
        # Also, Monday = 0 and Sunday = 6
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
        # Dead giveaway for using a staticmethod is if none of the class words get used

import datetime
myDate = datetime.date(2016, 7, 10)
# >>> python3 oop2.py
# False
# So 7/10/2016 is definitely either a Saturday or Sunday

print(Employee.is_workday(myDate))

empOne = Employee('Corey', 'Schafer', 50000)
empTwo = Employee('Test', 'Employee', 60000)
# This @classmethod raises the class variable (raiseAmt)'s value for all 
# instances of the class
Employee.set_raise_amount(1.05)
# But this Corey employee is more attractive than their coworker: Test
# So, let's give Corey a raise
# This won't work :: empOne.set_raise_amount(1.285)

# print(Employee.raiseAmt) # What should these return?
# print(empOne.raiseAmt)
# print(empTwo.raiseAmt)

# Making new instances from an unhelpfully formatted string
emStringZero = 'Will-Reilly-000120'
emStringOne = 'David-Golembiowski-590120'
emStringTwo = 'Cameron-Reilly-590210'
emStringThree = 'Paul-Olson-850910'

# One-liner for creating a single-time class instance
#   new_emp_str = Employee(first, last, pay)

# Improved one-liner for creating multiple class instances (per string)
new_emp_1 = Employee.from_str(emStringOne)