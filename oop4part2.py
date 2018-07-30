
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
emp_1 = Employee('Corey', 'Schafer', 50000)
emp_1 = Employee('Test', 'Employee', 60000)


mgr_1 = Manager('Sue', 'Smith', 90000, [dev_1])

# Is mgr_1 an instance of Employee class?
print(isinstance(mgr_1, Employee))
# Is mgr_1 an instance of Developer class?
print(isinstance(mgr_1, Developer))
# Is "Developer" a subclass of "Employee"?
print(issubclass(Developer, Employee))
# Is "Manager" a subclass of "Developer"?
print(issubclass(Manager, Developer))