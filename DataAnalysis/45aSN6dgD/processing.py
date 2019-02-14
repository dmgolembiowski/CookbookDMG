#!/usr/bin/env python3
# Processing.py 
import pandas as pd  
from collections import deque
from numpy import nan
import furtherProcessing

def process_descriptions(children, imitmidx_sql):
    """
    `process_descriptions()` accepts the children dictionary and 
    inserts a new value into the "description" index for each
    entry in children.
    """
    def description_composition(desc_One, desc_Two):
        s1 = desc_One if type(desc_One) is str else ""
        s2 = desc_Two if type(desc_Two) is str else ""
        return s1 + ", " + s2 if s1 and s2 else s1+s2

    list_o_item_no = [children[k]["item_no"].strip(' ') for k in list(children)]
    # Gather abstracted magic numbers
    item_num = furtherProcessing.itercolumns(imitmidx_sql, "item_no")
    item_desc_1 = furtherProcessing.itercolumns(imitmidx_sql, "item_desc_1")
    item_desc_2 = furtherProcessing.itercolumns(imitmidx_sql, "item_desc_2")
    for row in imitmidx_sql.itertuples():
        item_no = row[item_num].strip(' ')
        if item_no in list_o_item_no:
            description_one = row[item_desc_1]
            description_two = row[item_desc_2]
            updated_description = description_composition(description_one, description_two)
            for kid in list(children):
                if children[kid]["item_no"].strip(' ') == item_no:
                    children[kid]["description"] = updated_description

    return children

def get_costs(children, iminvloc):
    """
    `get_costs()` retrieves "avg_cost" and "last_cost" from 
    the iminvloc_sql pandas.DataFrame object. 
    For each of the materials in the list of children, 
    "avg_cost" and "last_cost" values are assigned to the
    appropriate children.
    """
    list_o_item_no = [children[k]["item_no"].strip(' ') for k in list(children)]

    for row in iminvloc.itertuples():
        item_no = row[1].strip(' ')
        if item_no in list_o_item_no:
            avg_cost = row[2]
            last_cost = row[3]
            for kid in list(children):
                if children[kid]["item_no"].strip(' ') == item_no:
                    children[kid]["avg_cost"] = avg_cost
                    children[kid]["last_cost"] = last_cost

    return children

def process_bill(children, bmprdstr):
    """
    `process_bill()` iterates through tuple rows of bmprdstr_sql,
    a pandas.DataFrame object, and checks for rows whose "item_row"
    index matches that of the children dictionary.
    If a match is identified then "qty_per_part" will be assigned a 
    value for its corresponding entry.

    Recall how the `bmprdstr_sql` SQLite table contained multiple rows
    with identical "item_no" text. For this reason, additional processing
    is needed to delete 
    """

    list_o_item_no = [children[k]["item_no"].strip(' ') for k in list(children)]

    for row in bmprdstr.itertuples():
        item_no = row[3].strip(' ')
        if item_no in list_o_item_no:
            qty_per_par = row[5]
            for kid in list(children):
                if children[kid]["item_no"].strip(' ') == item_no:
                    children[kid]["qty_per_par"] = qty_per_par
                    i = 0
                    while i < len(list_o_item_no):
                        if list_o_item_no[i].strip(' ') == item_no:
                            del(list_o_item_no[i])
                            break
                        i += 1

    return children
    
def get_children(current_item, bmprdstr_sql, imitmidx_sql):
    children = { 0: { 
        'ID':0,
        'item_no':current_item,
        'description': nan,
        'qty_per_par': 1,
        'avg_cost': nan,
        'last_cost': nan,
        'level': 0,
        'parent_ID':-1,
        'kids_IDs':[],
        'labor_hours':nan,
        'pur_or_mfg':nan,
        'calc_cost': nan} }

    #explored = set() #MARKED FOR REMOVAL
    visited = []
    frontier = deque()
    takenIDs = [-1]

    # Rename to `next_generation()`
    def next_generation(ID = 0, level=0, df=bmprdstr_sql, master=imitmidx_sql.to_dict()):    
        """
        Create a template of materials called "children" with indices/headers:
        example_row = ['ID','item_no', 'description', 'qty_per_par','avg_cost', 'last_cost', 'level', 'parent_ID']
        and map a material's ID to its dictionary key.

        DataFrames are powerful data containers for focusing data that meet certain criteria,
        but their structure makes programming search algorithims inconvenient, since
        these objects are not hashable or subscriptable. (Later on, it will be more sensible to use
        `billOfMaterials.to_dict('index')` once everything is in the billOfMaterials dataframe, but until then...)
     
        Therefore `generations()` returns an implicitly-ordered dictionary that where each material's
        ID returns a dictionary of its data template. Dictionaries make it simple to look up children
        of parents and parents of children. 

        Also, dictionaries are an acceptable data type to pass to the `data` argument of 
        the DataFrame constructor, which also pass the DataFrame's headers/column names to be used
        in the final Bill of Materials report in Microsoft Excel.
        """

        current_parent_ID = ID
        level += 1
        # furtherProcessing.itercolumns(bmprdstr_sql, "item_no")
        for row in df.itertuples():
            if row[1].strip(' ') == children[current_parent_ID]["item_no"].strip(' '):
                next_gen_ID = takenIDs[-1] +1
                takenIDs.append(next_gen_ID)
                successor = {
                    next_gen_ID:{
                        'ID':next_gen_ID,
                        'item_no':row[3],
                        'description':nan,
                        'qty_per_par':row[5],
                        'avg_cost':nan,
                        'last_cost':nan,
                        'level':level,
                        'parent_ID':current_parent_ID,
                        'kids_IDs':[],
                        'labor_hours':nan,
                        'pur_or_mfg':nan,
                        'calc_cost': nan}
                    }
                frontier.append(successor)

        # Give the child ID's to the parent object
        while frontier:
            this_child = frontier.popleft()

            key = list(this_child)[0]

            current_child = this_child[key]
            current_parent_ID = current_child['parent_ID']

            """ Added for debugging purposes; please keep
            {ID:{'ID':ID,'item_no':row[3].strip(' '),'description':nan,'qty_per_par':row[4],'avg_cost':nan,'last_cost':nan,'level':level,'parent_ID':current_parent_ID,'kids_IDs':[]}}
            print("children[current_parent_ID]['kids_IDs'] = ",children[current_parent_ID]['kids_IDs'])
            print("type(children[current_parent_ID]['kids_IDs']) = ", type(children[current_parent_ID]['kids_IDs']))
            input()
            """

            children[current_parent_ID]['kids_IDs'].append(current_child['ID'])

            visited.append(this_child)
            print('visited.append(current_child)',visited)
            children.update(this_child)

        """ 
        The next logical step is to retrieve succcessors to the child objects by
        popping elements from the "visited" list as new current_parents. 
        Add each of their ID's to the parent's "kids_IDs" list
        """

        while visited:
            child = visited.pop()
            children.update(child)
            childID = list(child)[0]
            child = child[childID]
            print(children)
            next_generation(ID=childID, level=child['level'])

    next_generation()
    return children
# Marked for removal
'''
def purchasedManufacturedDetail(imitmidx_sql, sfdtlfil_sql, children):
    number_rows_imitmidx = len(imitmidx_sql)
    number_rows_sfdtlfil_sql = len(sfdtlfil_sql)

    item_master = imitmidx_sql.to_dict('dict')
    shop_master = sfdtlfil_sql.to_dict('dict')
    
    imitmidx_sql_manufactured = {}
    imitmidx_sql_purchased = {}
    
    sfdtlfil_sql_manufactured = {}
    sfdtlfil_sql_purchased = {}
    #a = set(X.strip(' ') for X in [x if type(x) is str else "" for x in sfd['out_item_no']])
'''

def main(imitmidx_sql, iminvloc_sql, bmprdstr_sql, sfdtlfil_sql):
    """
    Calls `generate_children()` and other functions to yield a billOfMaterials
    pandas.DataFrame class object.
    """
    parent_item = input("Enter the parent item number: ")
    children = get_children(parent_item, bmprdstr_sql, imitmidx_sql)

    # Concatenate "item_desc_1" and "item_desc_2" from imitmidx_sql
    children = process_descriptions(children, imitmidx_sql)
    children = get_costs(children, iminvloc_sql)
    children = process_bill(children, bmprdstr_sql)

    # Now the good stuff
    bill = []
    i = 0
    while i < len(list(children)):
        bill.append(children[i])
        i += 1
    
    billOfMaterials = pd.DataFrame(data=bill)
    billOfMaterials.name = 'Materials'

    # Correctional punishment to billOfMaterials for not having its headers 
    # in the order originally prescribed
    billOfMaterials = billOfMaterials[['ID', 'item_no', 'description', 'qty_per_par', 'avg_cost', 'last_cost', 'level', 'parent_ID', 'kids_IDs', 'labor_hours', 'pur_or_man', 'true_cost']]

    """
    Potential Process Flow:



    """


    return billOfMaterials
