#!/usr/bin/env python3
from collections import namedtuple
from time import sleep

# Path to CSV File
PATH = "YOUR/PATH/TO/THEFILE"

# CrimeData is serving as the class
CrimeData = namedtuple('CrimeData', ['cDateTime',
    'address',
    'district',
    'beat',
    'grid',
    'crime_Description',
    'ucr_ncic_code',
    'latitude',
    'longitude'])

# Get rid of the random "________" that follows the 'beat' parameter
def removes_Eight_Spaces(csvString):
    return csvString.replace('        ', '')

"""
Process Flow of january.py:
    1. Read in the first line of PATH as a string
    2. Remove 8 empty characters from the 'beat' parameter
    3. Split the file_String along each '^M' into a list element
    4. Split each new list element along a "," then make a CrimeData object
        Put this object into crime_data
    5. Print each crime_data list element to the command line
"""

file_List = []
# Get the file into a python string
with open(PATH,'r') as f:
    for line in f:
        file_List.append(str(line))

print('Successfully gathered csv file contents into python string...')
print('Cleaning up data...')
sleep(2)

list_Of_CrimeData = []
i = 0
while i < len(file_List):
    file_List[i] = file_List[i].split(',')
    file_List[i][3] = file_List[i][3].rstrip()
    file_List[i][8] = file_List[i][8].replace("\n",'')
    list_Of_CrimeData.append(CrimeData(*file_List[i]))
    i += 1

for data in list_Of_CrimeData:
    print(data)
    for part in data:
        print(part)
    print()
