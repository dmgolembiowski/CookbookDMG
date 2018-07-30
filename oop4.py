
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
        
class Developer(Employee):
    raiseAmount = 1.10

    def  __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        # Alternative way: Employee.__init__(self, first, last, pay)
        self.prog_lang = prog_lang

class Manager(Employee):
    def  __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        # Alternative way: Employee.__init__(self, first, last, pay)
        # you never want to immutable data types
        # as 
        if employees is None:
            self.employees = [] # empty list
        else:
            self.employees = employees
    
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def rem_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
    
    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())

# dev_1 = Developer('Corey', 'Schafer', 50000)
# dev_2 = Developer('Test', 'Employee', 60000)
dev_1 = Developer('Corey', 'Schafer', 50000, 'Python')
dev_2 = Developer('Test', 'Employee', 60000, 'Java')
# print(help(Developer))
# print('Starting Salary: ' + str(dev_1.pay))
# dev_1.applyRaise()
# print('Starting Salary with 10 percent raise: ' + str(dev_1.pay))

mgr_1 = Manager('Sue', 'Smith', 90000, [dev_1])
print(mgr_1.email)
# At this point, Sue Smith already has Corey as a developer.
# So, we're going to print her developer employees.
print('Employees before adding new ones: ' )
mgr_1.print_emps()
# Next, I'm going to assign her the 'Test Employee' developer
print('Employees after adding new ones: ')
mgr_1.add_emp(dev_2)
mgr_1.print_emps()
# See now that Sue is assigned two developers
# Oh NO! Corey quit because of poor management under Sue.
# Let's remove Corey from the system.
mgr_1.rem_emp(dev_1)
print('Employees after removal: ')
mgr_1.print_emps()