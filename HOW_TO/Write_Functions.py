#!/usr/bin/env python3

# Here's a standard way to make a python function

def function_Name():
    d = 'a string to print'
    print(d)
  
def function_Name2(x):
    x = x + 2
    return x

def multivariate_Function(a,b,c):
    a = a - b -c
    b = b - a -c
    c = 2*(a + b)
    return a, b, c
    

# Below here can be like a main function (or not...)

# Print 'a string to print'
function_Name()

# Add 2 to some number
xPlusTwo = function_Name2(8413)

A, B, C = multivariate_Function(12, 1, 6)
print('A: ', A)
print('B: ', B)
print('C: ', C)
