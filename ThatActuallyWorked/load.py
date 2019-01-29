#!/usr/bin/env python3
# C:\Users\dGolembiowski\svn_repos\
# C:\Users\dGolembiowski\svn_repos\load.py
import sqlite3
import pandas as pd 
import numpy as np 
import pymssql
import os
import processing 

def database_tables():
    """
    `database_tables()` retrieves three pandas data frame objects of 
    the tables retrieved from the iecsa0600_099 database.
    Should return three separate objects: imitmidx_sql, iminvloc_sql, and bmprdstr_sql tables.
    
    Functions:
    `grab_imitmidx()`: SELECT item_no, item_desc_1, item_desc_2 FROM imitmidx_sql ORDER BY item_no;
    `grab_iminvloc()`: SELECT item_no, avg_cost, last_cost FROM iminvloc_sql ORDER BY item_no;
    `grab_bmprdstr()`: SELECT item_no, comp_item_no, alt_item_no, qty_per_par FROM bmprdstr_sql ORDER BY item_no;
    """ 

    # SQL Auth
    SERVER = ""
    USER = ""
    PASSWORD = ""
    DATABASE = ""
    
    def grab_imitmidx():
        return """
        SELECT item_no, item_desc_1, item_desc_2 FROM imitmidx_sql;"""

    def grab_iminvloc():
        return """
        SELECT item_no, avg_cost, last_cost FROM iminvloc_sql;"""

    def grab_bmprdstr():
        return "SELECT item_no, seq_no, comp_item_no, alt_item_no, qty_per_par FROM bmprdstr_sql;"

    # Socket
    connection = pymssql.connect(
        SERVER,
        USER,
        PASSWORD,
        DATABASE)
    
    imitmidx_sql = pd.read_sql(grab_imitmidx(), connection)
    iminvloc_sql = pd.read_sql(grab_iminvloc(), connection)
    bmprdstr_sql = pd.read_sql(grab_bmprdstr(), connection)

    return imitmidx_sql, iminvloc_sql, bmprdstr_sql

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


def write_local_tables(Itmidx, Invloc, Bmprdstr):
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

    # Write updated information to these tables
    Itmidx.to_sql(name='imitmidx_sql', con=Local_Connection)
    Invloc.to_sql(name='iminvloc_sql', con=Local_Connection)
    Bmprdstr.to_sql(name='bmprdstr_sql', con=Local_Connection)

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

    itmidx = pd.read_sql("SELECT * FROM imitmidx_sql", Local_Connection)
    invloc = pd.read_sql("SELECT * FROM iminvloc_sql", Local_Connection)
    bmprdstr =  pd.read_sql("SELECT * FROM bmprdstr_sql", Local_Connection)

    # Dropping pesky 'index' column of extra indices
    itmidx = itmidx.drop(columns=['index'])
    invloc = invloc.drop(columns=['index'])
    bmprdstr = bmprdstr.drop(columns=['index'])   

    return itmidx, invloc, bmprdstr

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
    imitmidx_sql, iminvloc_sql, bmprdstr_sql = database_tables()

    """
    Call `write_local_tables()` to write 
    pandas.DataFrame contents of "imitmidx_sql", "iminvloc_sql", and "bmprdstr_sql" 
    as SQL-formatted data -- returning the SQLite connection
    """
    Local_Connection = write_local_tables(imitmidx_sql, iminvloc_sql, bmprdstr_sql)

    """
    `read_local_tables()` accepts a "sqlite3.connection" object generated 
    by `write_local_tables()` to minimize the number of SQLite connections.
    Otherwise, if `load.read_local_tables()` is called in isolation on 
    the interpreter, a new SQLite connection is made. This function returns 
    pandas.DataFrame objects for each of the three tables.
    """
    imitmidx_sql, iminvloc_sql, bmprdstr_sql = read_local_tables(Local_Connection)
    """ # Return to this
    BillOfMaterials = processing.main(imitmidx_sql, iminvloc_sql, bmprdstr_sql)
    return BillOfMaterials"""
    billOfMaterials = processing.main(imitmidx_sql, iminvloc_sql, bmprdstr_sql)
    print(billOfMaterials) # Marked for removal
    return billOfMaterials

if __name__ == "__main__":
    main()



# Notes:
"""
✓ Set indices for each of the database tables in the sqlite databse 
✓ Install the DB Browser for SQLite
✓ Fix this including the os.delete database file at C:\\sqlite\099.db
"""
