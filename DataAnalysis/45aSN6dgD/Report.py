#!/usr/bin/env python3
# shopOrderReport.py
"""
Generate Bill of Materials

Given a user-defined item_no,
the program connects to the SQL
server and pipes a query to return
that part's full description, average
cost, last cost, level of succession,
and predecessor's row number.
"""
from furtherProcessing import itercolumns
import pandas as pd
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
        self.excel_Frame = DataFrame()
    
class BOMReport(Report):
    def __init__(self,bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct):
        super().__init__(bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct) 
        #Report.__init__(self,bom_dataframe)
        self.excel_Frame.name = 'Bill_of_Material_Products'

    def output(self):
        self.excel_Frame = DataFrame(data=self.excel_Frame, 
            columns=["ID", "qty_per_par", "item_no",
                "description","avg_cost", "last_cost", 
                "level", "parent_ID"])
        pass

    def defineBom(self, *args, **kwargs):
        pass

class CostReport(Report):
    def __init__(self, bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, billOfMaterialProduct):
        super().__init__(bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable) 
        # Report.__init__(self,bom_dataframe)

class Inventory:
    IDs = []
    def __init__(self, bom_Dataframe, *IDs, **materialArgs):
        self.bom_Dataframe = bom_Dataframe
        for id in IDs:
            Inventory.IDs.append(id)

class Material(Inventory):
    def __init__(self, bom_Dataframe, *IDs, **materialArgs):
        pass

    def __new__(material):
        #self = super().__new__(_, bom_Dataframe)
        for ID in Inventory.IDs:
            pass
        # Override 
        '''
        self.ID = self.bom_Dataframe["ID"]
        self.item_no = self.bom_Dataframe["item_no"].strip(' ')
        self.kids_IDs = self.Dom_dataframe["kids_IDs"]
        self.description = self.Dom
        '''
    
    def as_dict(self):
        return self.__dict__
    
    def __repr__(self):
        return "Material(%s)" % ", ".join(k +"="+repr(v) for k,v in self.__dict__.items())

