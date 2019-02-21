#!/usr/bin/env python3
# Analysis.py 
from Report import CostReport, Inventory, Item
import furtherProcessing
import numpy as np

def average(*args):
    avg = 0
    size = len(args)
    for number in args:
        avg += number
    return avg / size

def extrema(*args):
    min = 999999
    max = -1
    for value in args:
        if value < min:
            min = value
        elif value > max:
            max = value 
        else:
            pass
    return min, max

def median(*args):
    collection = []
    for value in args:
        collection.append(value)
    return np.median(collection)

def quartiles(*args):
    collection = []
    for value in args:
        collection.append(value)
    first_quartile = np.percentile(collection,25)
    third_quartile = np.percentile(collection,75)
    return first_quartile, third_quartile
