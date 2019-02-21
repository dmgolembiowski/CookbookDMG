#!/usr/bin/env python3
from collections import deque
import pandas as pd
from pandas import Timestamp
import Report

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
    elif len(colName) == 1:
        match = colName[0]
        for frame in dataframe.itertuples():
            columnsList = frame._asdict()
            columnsList = dict(columnsList)
            i = 0
            while i < len(columnsList):
                if list(columnsList)[i] == match:
                    return i
                i +=1
            break
        raise ValueError('DataFrame did not contain specified column header name')
    '''
        for column in columnsList:
            pass
        
    else:
        for frame in dataframe.itertuples():
            columnsList = list(frame._asdict())
            break
        i = 0
        while i < len(columnsList):
            breakpoint()
            dataframe_columns[columnsList[i]] = i
            i += 1
        return dataframe_columns[colName[0]]
    '''
    
def afterepoch(dataframe, completed_date='compl_dt'):
    """ 
    `after_epoch()` accepts a pd.Dataframe object and operates
    on a row which has the form:

    Pandas(Index=0, item_no='E000351-LT24                  ', 
        qty=1.0, act_lbr_hr=1.5, pur_or_mfg=None, pln_cost=0.0, 
        act_cost=37.5, out_item_no=None, 
        compl_dt=Timestamp('2016-04-15 00:00:00'), last_chg_dt=NaT)
    """
    #cols = [col for col in dataframe.columns]
    #after_epoch = pd.DataFrame(data=[], columns=cols)
    after_epoch = []
    compl_dt = itercolumns(dataframe, completed_date)
    print(compl_dt)

    for row in dataframe.itertuples():
        if type(row[compl_dt]) is not pd.NaT:
            if Timestamp(row[compl_dt]) >= epoch:
                after_epoch.append(dict(row._asdict()))
    after_epoch = pd.DataFrame(data=after_epoch)
    return after_epoch.drop('Index', 1)

# This function needs to be further abstracted to a dataframe that has any number of columns
def ManufacturedCost(dataframe):
    """
    Given an object like `dataframe`, must iterate through row tuples to
    change `None` type values to an 'M' string.
    Next, must convert 
    """
    pur_or_mfg = itercolumns(dataframe, "pur_or_mfg")
    outgoing_frames = []
    """
    The '_' column header is an artifact of needing to 
    preserve the number of columns in between a pandas.frame
    and a pandas.DataFrame
    """
    outgoing_column_headers = ['_','item_no', 'qty', 'act_lbr_hr', 'pur_or_mfg', 'pln_cost', 'act_cost', 'out_item_no', 'compl_dt']
    # Make this go for both imitmidx and sfdtlfil
    for frame in dataframe.itertuples():
        if type(frame[pur_or_mfg]) is type(None):
            intermediate_frame = [entry for entry in frame]
            intermediate_frame[pur_or_mfg] = "M"
            #intermediate_frame.insert(0,None) #Get around annoying AssertionError
            outgoing_frames.append(intermediate_frame)
        else: 
            intermediate_frame = [entry for entry in frame]
            intermediate_frame[pur_or_mfg] = "P"
            outgoing_frames.append(intermediate_frame)

    outgoing_frames = pd.DataFrame(data=outgoing_frames, columns=outgoing_column_headers)
    outgoing_frames = outgoing_frames[['item_no', 'qty', 'act_lbr_hr', 'pur_or_mfg', 'pln_cost', 'act_cost', 'out_item_no', 'compl_dt']]
    return outgoing_frames

# Marked for deletion: `uniquenames()` was absorbed by 
# `Report.CostReport.uniquenames()`
def uniquenames(dataframe):
    """ Collects distinct item_no's from the Shop order detail table """
    # Note: this function should accept the dataframe coming out of `afterepoch()`
    names = []
    item_no = itercolumns(dataframe, 'item_no')
    for name in dataframe.itertuples():
        if name[item_no].strip(' ') not in names:
            names.append(name[item_no].strip(' '))
    return names
