#!/usr/bin/env python3.7
import pandas as pd
import pymssql
import sqlite3
import numpy as np
import Report
import processing
import furtherProcessing

def main():
    """
    `read_local_tables()` accepts a "sqlite3.connection" object generated 
    by `write_local_tables()` to minimize the number of SQLite connections.
    Otherwise, if `load.read_local_tables()` is called in isolation on 
    the interpreter, a new SQLite connection is made. This function returns 
    pandas.DataFrame objects for each of the three tables.
    """
    #assert(Local_Connection is not None) # Marked for potential removal
    '''
    try:
        del Imitmidx, Invloc, Bmprdstr, Sfdtlfil, imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql
        gc.collect()
        gc.disable()
    except NameError:
        pass
    '''
    Local_Connection = sqlite3.connect("/mnt/c/sqlite/099.db")
    imitmidx_sql = pd.read_sql("SELECT * FROM imitmidx_sql;", Local_Connection)
    iminvloc_sql = pd.read_sql("SELECT * FROM iminvloc_sql;", Local_Connection)
    bmprdstr_sql =  pd.read_sql("SELECT * FROM bmprdstr_sql;", Local_Connection)
    sfdtlfil_sql = pd.read_sql("SELECT * FROM sfdtlfil_sql;", Local_Connection)
    # Dropping pesky "index" column of extra indices
    imitmidx_sql = imitmidx_sql.drop(columns=["index"])
    iminvloc_sql = iminvloc_sql.drop(columns=["index"])
    bmprdstr_sql = bmprdstr_sql.drop(columns=["index"])
    sfdtlfil_sql = sfdtlfil_sql.drop(columns=["index"]) 
    
    billOfMaterials, children = processing.main(imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql)

    sysargForGenReport = False
    if sysargForGenReport:
        bom_report = Report.BOMReport(billOfMaterials, imitmidx_sql, iminvloc_sql, sfdtlfil_sql, bmprdstr_sql)
        bom_report.output()

    # Starts the cost-reporting functionality
    inventory = Report.Inventory(bom_Dataframe=billOfMaterials, bom_Dict=children)
    item = Report.Item.item
    breakpoint()
    return imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql
