#!/usr/bin/env python3
# C:\Users\dGolembiowski\svn_repos\
# C:\Users\dGolembiowski\svn_repos\load.py
import sqlite3
import pandas as pd 
import numpy as np 
import pymssql
import os
import processing
import furtherProcessing
from furtherProcessing import afterepoch
import Report

#import gc 
#gc.disable()

def database_tables():
    """
    `database_tables()` retrieves three pandas data frame objects of 
    the tables retrieved from the iecsa0600_099 database.
    Should return three separate objects: imitmidx_sql, iminvloc_sql, and bmprdstr_sql tables.
    """ 

    # SQL Auth
    SERVER = ""
    USER = ""
    PASSWORD = ""
    DATABASE = ""
    
    def grab_imitmidx():
        return """
        SELECT item_no, item_desc_1, item_desc_2, pur_or_mfg FROM imitmidx_sql;"""

    def grab_iminvloc():
        return """
        SELECT item_no, avg_cost, last_cost FROM iminvloc_sql;"""

    def grab_bmprdstr():
        return "SELECT item_no, seq_no, comp_item_no, alt_item_no, qty_per_par FROM bmprdstr_sql;"

    def grab_sfdtlfil_sql():
        return """
        SELECT item_no, qty, act_lbr_hr, pur_or_mfg, pln_cost, act_cost, out_item_no, compl_dt FROM sfdtlfil_sql;"""

    # Socket
    connection = pymssql.connect(
        SERVER,
        USER,
        PASSWORD,
        DATABASE)
    
    imitmidx_sql = pd.read_sql(grab_imitmidx(), connection)
    iminvloc_sql = pd.read_sql(grab_iminvloc(), connection)
    bmprdstr_sql = pd.read_sql(grab_bmprdstr(), connection)
    sfdtlfil_sql = pd.read_sql(grab_sfdtlfil_sql(), connection)

    return imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql

def sqlite_connection(db_file):
    """
    Creates a database connection to the 099.db database file
    located at C:\\sqlite\099.db 
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except ConnectionRefusedError:
        print(ConnectionRefusedError)
    return None


def write_local_tables(Itmidx, Invloc, Bmprdstr, Sfdtlfil):
    """
    `write_local_tables()` accepts three pandas.DataFrame objects 
    to write to C://sqlite/099.db as database tables. It returns 
    a connection to the SQLite database for use in 
    `read_local_tables()`.
    """
    PATH = "099.db"

    try:
        os.remove(PATH) # Make this line a comment before running in Debian WSL
        # os.remove("/mnt/c/sqlite/099.db") # Uncomment this line for usage in Debian WSL
    except PermissionError:
        with open(PATH, 'w') as f:
            f.close()

    #with open(PATH, 'w'):
    Local_Connection = sqlite_connection(PATH)
    assert(Local_Connection is not None)

    # Write only data beyond 9-29-2016 to Sfdtlfil_sql
    Sfdtlfil = afterepoch(Sfdtlfil)

    # Write updated information to these tables
    Itmidx.to_sql(name='imitmidx_sql', con=Local_Connection)
    Invloc.to_sql(name='iminvloc_sql', con=Local_Connection)
    Bmprdstr.to_sql(name='bmprdstr_sql', con=Local_Connection)
    Sfdtlfil.to_sql(name="sfdtlfil_sql", con=Local_Connection)
    return Local_Connection

def read_local_tables(Local_Connection = sqlite3.connect("C://sqlite/099.db")):
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
    imitmidx_sql = pd.read_sql("SELECT * FROM imitmidx_sql;", Local_Connection)
    iminvloc_sql = pd.read_sql("SELECT * FROM iminvloc_sql;", Local_Connection)
    bmprdstr_sql =  pd.read_sql("SELECT * FROM bmprdstr_sql;", Local_Connection)
    sfdtlfil_sql = pd.read_sql("SELECT * FROM sfdtlfil_sql;", Local_Connection)
    # Dropping pesky "index" column of extra indices
    imitmidx_sql = imitmidx_sql.drop(columns=["index"])
    iminvloc_sql = iminvloc_sql.drop(columns=["index"])
    bmprdstr_sql = bmprdstr_sql.drop(columns=["index"])
    sfdtlfil_sql = sfdtlfil_sql.drop(columns=["index"]) 

    return imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql

def main():
    """
    For the impatient:
        import load, processing
        billOfMaterials = load.main()
        
    Process Flow:
    I. `main()` calls `database_tables()` to return three values
        (imitmidx_sql, iminvloc_sql, bmprdstr_sql) which are each 
        pandas.DataFrame objects collected from locally-written 
        copies of the Macola server
        A. `write_local_tables()` first removes 099.db file if 
            already exists
        C. `write_local_tables()` calls `sqlite_connection()` to 
            return a SQLite3 connection, assigned as "Local_Connection"
            in `main()`
    II. `main()` calls `read_local_tables()` passing the connection
        (from previous step) returning local copies of the SQLite data
        as pandas.DataFrame objects.
    III. `processing.main()` returns pandas.DataFrame object, called billOfMaterials,
        that is prepared mostly by `processing.get_children()` and its
        child function `processing.next_generation()`. 
    """

    """
    Collect data with `database_tables() from Macola 099 database
    tables: imitmidx_sql, iminvloc_sql, and bmprdstr_sql,
    and store the results as pandas.DataFrame objects
    """
    imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql = database_tables()

    """
    Call `write_local_tables()` to write 
    pandas.DataFrame contents of "imitmidx_sql", "iminvloc_sql", and "bmprdstr_sql" 
    as SQL-formatted data -- returning the SQLite connection
    """
    Local_Connection = write_local_tables(imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql)

    """
    `read_local_tables()` accepts a "sqlite3.connection" object generated 
    by `write_local_tables()` to minimize the number of SQLite connections.
    Otherwise, if `load.read_local_tables()` is called in isolation on 
    the interpreter, a new SQLite connection is made. This function returns 
    pandas.DataFrame objects for each of the three tables.
    """
    imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql = read_local_tables(Local_Connection)
    """ # Return to this
    BillOfMaterials = processing.main(imitmidx_sql, iminvloc_sql, bmprdstr_sql)
    return BillOfMaterials"""
    billOfMaterials, children = processing.main(imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql)
    breakpoint()
    print(billOfMaterials) # Marked for removal
    #billOfMaterials, children = furtherProcessing.main(billOfMaterials, children, sfdtlfil_sql, bmprdstr_sql, imitmidx_sql, iminvloc_sql)
    
    sysargForGenReport = False
    if sysargForGenReport:
        bom_report = Report.BOMReport(billOfMaterials, imitmidx_sql, iminvloc_sql, sfdtlfil_sql, bmprdstr_sql)
        bom_report.output()

    # Starts the cost-reporting functionality
    inventory = Report.Inventory(bom_Dataframe=billOfMaterials, bom_Dict=children)
    item = Report.Item.item
    """
    Members of the Item class can also be accessed from 


    #bom_Report = Report.BOMReport(bom_Report)

    return billOfMaterials, children, materials
    """
if __name__ == "__main__":
    main()



# Notes:
"""
✓ Set indices for each of the database tables in the sqlite databse 
✓ Install the DB Browser for SQLite
✓ Fix this including the os.delete database file at C:\\sqlite\099.db
"""
