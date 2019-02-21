#!/usr/bin/env python3
# shopOrderReport.py
"""
Generate Bill of Inventory

Given a user-defined item_no,
the program connects to the SQL
server and pipes a query to return
that part's full description, average
cost, last cost, level of succession,
and predecessor's row number.
"""
import furtherProcessing
import pandas as pd
import numpy as np
from pandas import DataFrame
import openpyxl
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Report:
    def __init__(self, bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct):
        self.bom_Dataframe = bom_Dataframe
        self.itemMasterTable = itemMasterTable
        self.itemLocationTable = itemLocationTable
        self.shopOrderDetailTable = shopOrderDetailTable
        self.billOfMaterialProduct = billOfMaterialProduct
        self.excel_Frame = pd.DataFrame()
    
    
class BOMReport(Report):
    def __init__(self,bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct):
        super().__init__(bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct) 
        self.excel_Frame.name = 'Bill_of_Material_Products'

    def output(self):
        self.file_name = 'bom_' + self.bom_Dataframe.to_dict()['item_no'][0] + '.xslx'
        self.excel_Frame = DataFrame(data=self.bom_Dataframe)
        try:
            for c in ['ID', 'item_no', 'description', 'kids_IDs']:
                if c not in self.excel_Frame.columns:
                    print('This dataframe is missing minimum required columns for processing!')
                    print('Please double-check that the BOM dataframe has columns inlcuding: "ID", "item_no", "description", and "kids_IDs"')
                    raise KeyError
        except:
            pass

        self.excel_Frame = self.excel_Frame[['ID', 'item_no', 'description', 'kids_IDs']]
        self.writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')
        self.excel_Frame.to_excel(self.writer, sheet_name=self.bom_Dataframe.to_dict()['item_no'][0])
        self.writer.save()

class CostReport(Report):
    data = {}
    
    def __init__(self, bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct):
        super().__init__(bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct) 
        self.shopOrderDetailTable = furtherProcessing.afterepoch(shopOrderDetailTable)
        CostReport.bom_Dataframe = self.bom_Dataframe
        CostReport.itemMaterTable = self.itemMasterTable
        CostReport.shopOrderDetailTable = self.shopOrderDetailTable
        CostReport.billOfMaterialProduct = self.billOfMaterialProduct
        CostReport.names = CostReport.uniquenames()
        

    @classmethod
    def uniquenames(cls):
        names = []
        item_number = -1
        for frame in cls.shopOrderDetailTable.itertuples():
            item_number = frame[furtherProcessing.itercolumns(cls.shopOrderDetailTable, 'item_no')]
            break
        for frame in cls.shopOrderDetailTable.itertuples():
            if frame[item_number].strip(' ') not in names:
                names.append(frame[item_number].strip(' '))
        return names

    @staticmethod
    def average(*args):
        avg = 0
        size = len(args)
        for number in args:
            avg += number
        return avg / size

    @staticmethod
    def get_ranges(dataframe, some_unique_item_no):
        some_unique_item_no = some_unique_item_no.strip(' ')
        matches = []
        for frame in dataframe.itertuples():
            magic_column_number = furtherProcessing.itercolumns(dataframe, 'item_no')
            break
        for frame in dataframe.itertuples():
            if frame[magic_column_number].strip(' ') == some_unique_item_no:
                matches.append(dict(frame._asdict()))
            return matches

    def output(self, ShopOrderOverride=False):
        self.file_name = 'cost_report_' + self.bom_Dataframe.to_dict()['item_no'][0] + '.xslx'
        self.excel_Frame = DataFrame(data=self.bom_Dataframe)
        if not ShopOrderOverride:
            try:
                for c in ["ID", "qty", "item_no", "description", "kids_IDs", "avg_material_cost", "avg_hrs"]:
                    if c not in self.excel_Frame.columns:
                        print('This dataframe is missing minimum required columns for processing!')
                        print('Please double-check that the BOM dataframe has columns inlcuding: "ID", "qty", "item_no", "description", "kids_IDs", "avg_material_cost", "avg_hrs"')
                        raise KeyError
            except:
                pass
        else:
            pass
        self.excel_Frame = self.excel_Frame[['ID', 'item_no', 'description', 'kids_IDs']]
        self.writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')
        self.excel_Frame.to_excel(self.writer, sheet_name=self.bom_Dataframe.to_dict()['item_no'][0])
        self.writer.save()

class Inventory:
    IDs = []
    catalog = {}
    # bom_Dict should == children from processing.py 
    def __init__(self, bom_Dataframe, bom_Dict):
        self.bom_Dataframe = bom_Dataframe
        self.bom_Dict = bom_Dict
        self.IDs = list(self.bom_Dict)
        for ID in self.IDs:
            Inventory.IDs.append(ID)
        for ID in Inventory.IDs:
            Inventory.catalog[self.bom_Dataframe.to_dict('index')[ID]['ID']] = self.bom_Dict[ID]
            Item.item[ID] = Item(ID).__dict__

class Item:
    item = {}
    def __init__(self, ID):    
        self.ID = ID 
        self.item_no = Inventory.catalog[self.ID]['item_no']
        self.description = Inventory.catalog[self.ID]['description']
        self.qty_per_par = Inventory.catalog[self.ID]['qty_per_par']
        self.avg_cost = Inventory.catalog[self.ID]['avg_cost']
        self.last_cost = Inventory.catalog[self.ID]['last_cost']
        self.level = Inventory.catalog[self.ID]['level']
        self.parent_ID = Inventory.catalog[self.ID]['parent_ID']

        if Inventory.catalog[self.ID]['labor_hours'] == np.nan:
            self.labor_hours = 0
        else:
            self.labor_hours = Inventory.catalog[self.ID]['labor_hours']


        if Inventory.catalog[self.ID]['calc_cost'] == np.nan:
            self.calc_cost = 0
        else:
            self.calc_cost = Inventory.catalog[self.ID]['calc_cost']


        if Inventory.catalog[self.ID]['kids_IDs'] == []:
            self.kids_IDs = None
        elif len(Inventory.catalog[self.ID]['kids_IDs']) == 1:
            self.kids_IDs = Inventory.catalog[self.ID]['kids_IDs'][0]
        else:
            self.kids_IDs = Inventory.catalog[self.ID]['kids_IDs']


        if type(self.kids_IDs) is not type(None):
            self.pur_or_mfg = "M"
        else:
            self.pur_or_mfg = "P"
'''
THE GRAVEYARD OF DECEASED PREMATURE FUNCTIONS:

data = { ID : {
                "item_no" : Item.item[ID]["item_no"],
                "avg_mt_cost" : average(row_entry_1[act_cost_col_number], row_entry_2[act_cost_col_number], ..., row_entry_M[act_cost_col_number]) -> $33.33,
                "avg_hours" : average(row_entry[act_hrs_col_number], ..., row_entry_N[act_hrs_col_number]) -> 4.00053, 
                } 
        }


# Marked for deletion FROM furtherProcessing.py
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
    return manufactured_list

def average(*args):
    avg = 0
    size = len(args)
    for number in args:
        avg += number
    return avg / size

def get_ranges(dataframe, some_unique_item_no):
    some_unique_item_no = some_unique_item_no.strip(' ')
    matches = []
    for frame in dataframe.itertuples():
        magic_column_number = furtherProcessing.itertuples(dataframe, 'item_no')
        break
    for frame in dataframe.itertuples():
        if frame[magic_column_number].strip(' ') == some_unique_item_no:
            matches.append(dict(frame._asdict()))
        return matches

"""
def main(billOfMaterials, children, sfdtlfil_sql, bmprdstr_sql, imitmidx_sql, iminvloc_sql):

    sfdtlfil_sql = afterepoch(sfdtlfil_sql)
    #billOfMaterials = ManufacturedCost(billOfMaterials)
    return billOfMaterials, children
"""
'''
