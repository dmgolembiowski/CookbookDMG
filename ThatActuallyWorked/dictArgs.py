#!/usr/bin/env python3

def values(x):
    for keys in x:
        print('x['+str(keys)+'] =', x[keys])

aDictionary = {
        'first':'is the worst',
        'second':'is the best',
        'third':'is the one with the treasure chest'}

values(aDictionary)
"""
$ ./dictArgs.py
x[first] = is the worst
x[second] = is the best
x[third] = is the one with the treasure chest
"""
