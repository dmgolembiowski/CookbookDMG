#!/usr/bin/env python3
from collections import deque
import pandas as pd
from pandas import Timestamp
# Boolean expressions can be used on "Timestamp",
# such as >, <, ==

epoch = Timestamp('2016-09-29 00:00:00')
item_master = pd.DataFrame()
# annoyingly inconsistent table header
# has Timestamp() repr in pd.itertuples()

def itercolumns(dataframe, *colName):
    """ 
    `itercolumns(pandas.DataFrame)` is a meaningful way to
    evaluate frames of pandas.DataFrame.itertuples() objects if
    the pandas.DataFrame gains or loses columns such that
    when iterating over pandas.DataFrame.itertuples()
    the pandas.core.frame in the iteration loses a previously
    accurate tuple position in the frame.

    In English:
        This method makes it possible to prepare data analysis 
        scripts that are resilient to fluctuating SQL databases 
        that keep the same column names, however their column
        slice can change as a result of adding or dropping a table.

    Derive from:
        Pandas(Index=0, component_item='E000404-C01',ID=10217.0)
    
    Returning:
        {'Index': 0, 'component_item': 1, 'ID': 2}
    """

    if len(list(colName)) > 1:
        raise ValueError('*colName cannot accept more than one column name')
    dataframe_columns = {}

    if len(colName) == 0:
        for frame in dataframe.itertuples():
            columnsList = list(frame._asdict())
            break
        i = 0
        while i < len(colName):
            dataframe_columns[columnsList[i]] = i
            i += 1
        return dataframe_columns
    else:
        for frame in dataframe.itertuples():
            columnsList = list(frame._asdict())
            break
        i = 0
        while i < len(columnsList):
            dataframe_columns[columnsList[i]] = i
            i += 1
        return dataframe_columns[colName[0]]
    
def afterepoch(sftdlfil_sql):
    """ 
    `after_epoch()` accepts a pd.Dataframe object and operates
    on a row which has the form:

    Pandas(Index=0, item_no='E000351-LT24                  ', 
        qty=1.0, act_lbr_hr=1.5, pur_or_mfg=None, pln_cost=0.0, 
        act_cost=37.5, out_item_no=None, 
        compl_dt=Timestamp('2016-04-15 00:00:00'), last_chg_dt=NaT)
    """

    after_epoch = pd.DataFrame(data=[], columns=[
        'item_no', 
        'qty',
        'act_lbr_hr',
        'pur_or_mfg',
        'pln_cost',
        'act_cost',
        'out_item_no',
        'compl_dt'])

    compl_dt = itercolumns(sftdlfil_sql, 'compl_dt')
    print(compl_dt)
    after_epoch = []

    for row in sftdlfil_sql.itertuples():
        if type(row[compl_dt]) is not pd.NaT:
            if row[compl_dt] >= epoch:
                after_epoch.append(row)
                
    temp = deque(_ for _ in after_epoch)
    temp_dict = []
    i = 0
    while temp:
        # Needs better code:
        current = temp.pop()
        temp_dict.append({ 
            'item_no':current[1], 
            'qty': current[2],
            'act_lbr_hr':current[3],
            'pur_or_mfg':current[4],
            'pln_cost':current[5],
            'act_cost':current[6],
            'out_item_no':current[7],
            'compl_dt':current[8]})
        i += 1
    sftdlfil_sql = pd.DataFrame(data=temp_dict, columns=['item_no', 'qty','act_lbr_hr','pur_or_mfg','pln_cost','act_cost','out_item_no','compl_dt','last_chg_dt'])
    return sftdlfil_sql

# Marked for removal
'''
def NoneToManufactured(dataframe):

    return dataframe
'''
# Transition to class method as CostReport.Manufactured()Report.py
def ManufacturedCost(billOfMaterials, imitmidx, sfdtlfil):
    """
    Given an object like `dataframe`, must iterate through row tuples to
    change `None` type values to an 'M' string.
    Next, must convert 
    """
    pur_or_mfg_Master = itercolumns(billOfMaterials, "pur_or_mfg")
    pur_or_mfg_Shop = itercolumns(sfdtlfil, "pur_or_mfg")

    # Make this go for both imitmidx and sfdtlfil
    for frame in billOfMaterials.itertuples():
        if frame[pur_or_mfg_Master] is None:
            r = frame[0] # The row number that disregards whether the table is changed later
            billOfMaterials.loc['pur_or_mfg',r] = "M"
    '''
    Do things
    '''
    return billOfMaterials


def unique_names(dataframe):
    """ Collects distinct item_no's from the Shop order detail table """
    # Note: this function should accept the dataframe coming out of `afterepoch()`
    names = []
    item_no = itercolumns(dataframe, 'item_no')
    for name in dataframe.itertuples():
        if name[item_no].strip(' ') not in names:
            names.append(name[item_no].strip(' '))
    return names


# Marked for deletion
def expand(dataframe):
    manufactured = deque()
    manufactured_list = []
    _ = itercolumns(dataframe)
    pln_cost = _['pln_cost']
    act_cost = _['act_cost']
    for row in dataframe.itertuples():
        if row[pln_cost] == 0.0 or row[act_cost] == 0.0 :
            manufactured.append(row)
    while manufactured:
        manufactured_list.append(manufactured.pop())
    return manufactured_list, 

def main(billOfMaterials, children):
    """

    """
    billOfMaterials = afterepoch(billOfMaterials)
    billOfMaterials = NoneToManufactured(billOfMaterials)

"""
Enter the SQL query: import q; sfdtlfil=q.sql(); import load; bom = load.main(); SELECT item_no, qty, act_lbr_hr, pur_or_mfg, pln_cost, act_cost, out_item_no, compl_dt, last_chg_dt FROM sfdtlfil_sql;
>>> rec
>>> 
                              item_no    qty  act_lbr_hr pur_or_mfg  pln_cost  act_cost out_item_no   compl_dt last_chg_dt
0      CS-000709-R                       1.0        0.00          P     87.00     87.00        None        NaT  2019-01-04
1      CS-000709-R                       1.0        0.00          P    221.98    221.98        None        NaT  2019-01-04
2      CS-000709-R                       1.0        0.00          P   1021.86   1021.86        None        NaT  2019-01-04
3      CS-000709-R                       1.0        0.00          P     81.14     81.14        None        NaT  2019-01-04
4      CS-000709-R                       1.0        0.00          P     98.00     98.00        None        NaT  2019-01-04
5      CS-000709-R                       1.0        0.00          P    120.57    120.57        None        NaT  2019-01-04
6      CS-000709-R                       1.0        0.00          P    592.27    592.27        None        NaT  2019-01-04
7      CS-000709-R                       1.0        0.00          P      0.20      0.20        None        NaT  2019-01-04
8      REWORK                            1.0        0.00          P      5.55      5.55        None        NaT  2019-01-04
9      REWORK                            1.0        0.00          P     28.38     28.38        None        NaT  2019-01-04
10     WRWMA3025-003-C28                17.0        0.00          M    170.00    649.16        None        NaT  2019-01-03
11     WRWMA3025-002-C28                33.0        0.00          M   1654.41   1671.01        None        NaT  2019-01-03
12     WRWMA3025-001-C28                33.0        0.00          M   1654.41   1669.41        None        NaT  2019-01-03
13     WRWMA3025-003                    17.0        0.50       None      0.00     10.00        None 2019-01-03         NaT
14     WRWMA3025-003                    17.0        0.00          P    639.16    639.16        None        NaT  2019-01-03
15     WRWMA3025-002                    33.0        0.83       None      0.00     16.60        None 2019-01-03         NaT
16     WRWMA3025-002                    33.0        0.00          M   1654.41   1654.41        None        NaT  2019-01-03
17     WRWMA3025-001                    33.0        0.75       None      0.00     15.00        None 2019-01-03         NaT
18     WRWMA3025-001                    33.0        0.00          M   1654.41   1654.41        None        NaT  2019-01-03
19     CS-000643                         1.0        0.00       None      0.00      0.00        None 2018-12-27         NaT
20     CS-000643                         1.0        0.00          M   1251.98      0.00        None        NaT  2018-12-27
21     CS-000643                         1.0        0.00          M    588.63      0.00        None        NaT  2018-12-27
22     CS-000643                         1.0        0.00          M    346.00      0.00        None        NaT  2018-12-27
23     E000038                           1.0        0.00          M   3967.27   3967.27        None        NaT  2018-12-27
24     E000908-L100                      1.0        0.00          P     22.60     22.60        None        NaT  2018-12-31
25     E000908-L100                    100.0        0.00          P    354.13    354.13        None        NaT  2018-12-31
26     E000908-L100                      2.0        0.00          P     17.83     17.83        None        NaT  2018-12-31
27     E000908-L100                      2.0        0.00          P      9.32      9.32        None        NaT  2018-12-31
28     E000908-L100                      1.0        0.00          P     27.52     27.52        None        NaT  2018-12-31
29     E000908-L100                      1.0        0.00          P     24.77     24.77        None        NaT  2018-12-31
...                               ...    ...         ...        ...       ...       ...         ...        ...         ...

Given an object like `rec`, must iterate through row tuples to
change `None` type values to an 'M' string.
Next, must convert 

cols = itercolumns(rec)
pur_or_mfg = cols["pur_or_mfg"]
for frame in dataframe.itertuples():
    if frame[pur_or_mfg] is None:
        i = itercolumns(rec)
        i = i["Index"]
        dataframe['pur_or_mfg'][i] = "M"
"""
